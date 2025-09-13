import os
import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from .security import verify_message
from .utils import get_message_type, log_payload, parse_response, get_media_url, download_media, send_message, get_message_status

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
    
@verify_message
def handle_message():
    payload = request.get_json()
    message_status = get_message_status(payload)
    if not payload:
        return jsonify({"status": "error", "message": "Invalid JSON provided"}), HTTPStatus.BAD_REQUEST.value
    if message_status:
        logging.info(f"Message status update received - {message_status.upper()}")
        return jsonify({"status": "ignored", "message": "No message to process"}), HTTPStatus.OK.value
    
    log_payload(payload)
    if get_message_type(payload) == 'image':
        media_url = get_media_url(payload)
        if media_url:
            save_path = os.path.join(os.getenv("MEDIA_DIR", "./media"), f"{parse_response(payload)[0]}.jpg")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            download_media(media_url, save_path)
            send_message("Image received and saved!")
    else:
        send_message("Message received!")
    return jsonify({"status": "success"}), HTTPStatus.OK.value
    

@webhook.route("/whatsapp", methods=["GET"])
def webhook_verify():
    return verify()

@webhook.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    return handle_message()