import os
import logging
import pprint
import requests
from http import HTTPStatus

BASE_URL = "https://graph.facebook.com"

def prepare_url(endpoint: str) -> str:
    version = os.getenv("META_API_VERSION")
    url = f"{BASE_URL}/{version}/{endpoint}"
    return url

def get_message_body(to: str, msg: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": msg
        }
    }

def send_message(msg: str) -> tuple:
    version = os.getenv("META_API_VERSION")
    phone_id = os.getenv("PHONE_NUMBER_ID")
    url = f"{BASE_URL}/{version}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    payload = get_message_body(os.getenv('RECIPIENT_WAID'), msg)
    
    response = requests.post(url, json=payload, headers=headers)
    if not HTTPStatus(response.status_code).is_success:
        logging.error(f"Failed to send message: {pprint.pformat(response.json())}")
    else:
        logging.info(f"Message sent: {msg} - ({response.status_code})")
    return response.json(), response.status_code

def get_sender(payload: dict) -> str:
    try:
        return (payload.get("entry", [])[0]
                .get("changes", [])[0]
                .get("value", {})
                .get("messages", [])[0]
                .get("from", "")).strip()
    except (IndexError, AttributeError):
        return None
        
def get_message_type(payload: dict) -> str:
    try:
        return (payload.get("entry", [])[0]
                .get("changes", [])[0]
                .get("value", {})
                .get("messages", [])[0]
                .get("type", ""))
    except (IndexError, AttributeError):
        return None
    
def get_message_status(payload: dict) -> str:
    try:
        return (payload.get("entry", [])[0]
                .get("changes", [])[0]
                .get("value", {})
                .get("statuses", [])[0]
                .get("status", ""))
    except (IndexError, AttributeError):
        return None

def get_image_id(payload: dict) -> str:
    return (payload.get("entry", [])[0]
            .get("changes", [])[0]
            .get("value", {})
            .get("messages", [])[0]
            .get("image", {})
            .get("id", ""))

def parse_response(payload: dict):
    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        from_number = changes.get("value", {}).get("messages", [])[0].get("from", "")
        body = changes.get("value", {}).get("messages", [])[0].get("text", {}).get("body", "")
        message_type = changes.get("value", {}).get("messages", [])[0].get("type", "")
        msg_id = changes.get("value", {}).get("messages", [])[0].get("id", "")
        return msg_id, from_number, body, message_type
    except (IndexError, AttributeError):
        return None

def get_body(payload: str):
    try:
        return (payload.get("entry", [])[0]
                .get("changes", [])[0]
                .get("value", {})
                .get("messages", [])[0]
                .get("text", {})
                .get("body", ""))
    except (IndexError, AttributeError):
        return None
    
def get_media_url(payload: dict):
    media_id = get_image_id(payload)
    url = prepare_url(media_id)
    
    logging.info(f"Media ID: {media_id}")
    logging.info(f"Requesting Media URL from: {url}")
    
    headers = {
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        media_url = response.json().get("url", "")
        return media_url
    else:
        logging.error(f"Failed to get media URL. Status code: {response.status_code}")
        return None

def download_media(media_url: str, save_path: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    if not media_url:
        logging.error("No media URL found.")
        return
    response = requests.get(media_url, headers=headers)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Media downloaded to {save_path}")
        return save_path
    else:
        logging.error(f"Failed to download media from {media_url}. Status code: {response.status_code}")
        logging.error(f"Response: {response.text}")
    
def log_payload(payload: str):
    _ ,number, body, message_type = parse_response(payload)
    logging.info(f"Received message from {number} ({message_type}): {body}")