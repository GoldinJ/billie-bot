import os
import pprint
import logging
from uuid import uuid1
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from splitwise.exception import SplitwiseException

from .services.invoice_processor.proccessor import InvoiceProcessor, Invoice
from .services.splitwise.spitwise_utils import create_expense, post_expense

from .security import verify_message
from .utils import get_message_type, log_response, get_media_url, download_media, send_message, get_message_status

logger = logging.getLogger(__name__)
webhook = Blueprint('webhook', __name__)

# Required webhook verifictaion for WhatsApp
def verify():
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == os.getenv("META_VERIFICATION_TOKEN"):
            # Respond with 200 OK and challenge token from the request
            logger.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logger.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), HTTPStatus.FORBIDDEN.value
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logger.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), HTTPStatus.BAD_REQUEST.value

def handle_expense(invoice: Invoice, file_path: str):
    if invoice is None:
        logging.error("Failed to process invoice")
        return jsonify({"error": "Failed to process invoice"}), HTTPStatus.RESET_CONTENT.value
    
    group_id = os.getenv("SPLITWISE_GROUP_ID")
    expense = create_expense(group_id, invoice, file_path)
    if expense is None:
        logging.info("Unsupported invoice type")
        send_message("Unsupported invoice type")
        return jsonify({"error": "Unsupported invoice type"}), HTTPStatus.RESET_CONTENT.value
    
    _id, errors = post_expense(expense)
    logging.debug(f"New expense created: {_id}")
    
    if errors:
        send_message("Some errors, happened while trying to post expense. See log for further detais...")
        return jsonify({"error": "Failed to post invoice"}), HTTPStatus.BAD_REQUEST.value
    else:
        send_message(f"*New expense created*:\nDescription - *{invoice.description}*\nCost - *{invoice.cost}*")
        
    return "", HTTPStatus.CREATED.value

def handle_media(response: dict, mtype:str="image"):
    extension_map = {
        "image": "jpg",
        "document": "pdf"
    }
    ext = extension_map.get(mtype, None)
    if not ext:
        send_message("Unsupported media type.")
        return "", HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value
    try:
        media_url = get_media_url(response)
        if media_url:
            uuid = str(uuid1())
            save_path = os.path.join(os.getenv("MEDIA_DIR", "./media"), f"{uuid}.{ext}")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file_path = download_media(media_url, save_path)
            invoice = InvoiceProcessor(file_path).process_invoice()
            response = handle_expense(invoice, file_path)
            return response
        else:
            send_message("No media found.")
            return jsonify({"error": "No media found"}), HTTPStatus.BAD_REQUEST.value
    except SplitwiseException as e:
        logging.error(exc_info=True)
        send_message("Some error happened. Failed to create an expense")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value
    except Exception as e:
        logging.error(e, exc_info=True)
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR.value

@verify_message
def handle_message():
    response = request.get_json()
    message_status = get_message_status(response)
    log_response(response)
    if not response:
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), HTTPStatus.BAD_REQUEST.value
    if message_status:
        logging.info(f"Message status update received - {message_status.upper()}")
        return jsonify({"status": "ignored", "message": "No message to process"}), HTTPStatus.OK.value
    
    mtype = get_message_type(response)
    if mtype != "text":
        response = handle_media(response, mtype)
        return response
    else:
        send_message("Message received!")
        
    return jsonify({"status": "success"}), HTTPStatus.OK.value
    

@webhook.route("/whatsapp", methods=["GET"])
def webhook_verify():
    return verify()

@webhook.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    return handle_message()