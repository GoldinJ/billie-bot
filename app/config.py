import os
import json
from dotenv import load_dotenv
from logging.config import dictConfig

def load_environment():
    load_dotenv()

def configure_logging():
    os.makedirs(r'./logs', exist_ok=True)
    with open(os.getenv("LOGGING_CONFIG"), "r") as f:
        config = json.load(f)
    dictConfig(config)
