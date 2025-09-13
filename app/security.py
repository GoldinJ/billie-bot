import os
import hmac
import hashlib
import logging
from http import HTTPStatus
from flask import request, jsonify


def verify_message(fn):
    def wrapper(*args, **kwargs):
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature:
            logging.warning("Missing signature")
            return jsonify({"status": "error", "message": "Missing signature"}), HTTPStatus.FORBIDDEN.value

        app_secret = os.getenv("META_APP_SECRET").encode()
        payload = request.get_data()
        expected_signature = 'sha256=' + hmac.new(app_secret, payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_signature, signature):
            logging.warning("Invalid signature")
            return jsonify({"status": "error", "message": "Invalid signature"}), HTTPStatus.FORBIDDEN.value
        
        logging.info("Signature verified")
        return fn(*args, **kwargs)
    return wrapper