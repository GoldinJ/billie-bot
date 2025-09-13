from flask import Flask
from .config import load_environment, configure_logging
from .routes import webhook

def create_app():
    
    load_environment()
    configure_logging()
    
    app = Flask(__name__)
    app.register_blueprint(webhook)
    
    return app