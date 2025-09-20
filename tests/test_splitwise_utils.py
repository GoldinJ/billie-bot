import os
import pytest
from splitwise.exception import SplitwiseNotAllowedException
from app.services.invoice_processor.invoice import Invoice
from app.services.splitwise.spitwise_utils import (
    create_expense,
    post_expense
)

@pytest.fixture
def invoice():
    raw_data = {
        "from_date": {
            "confidence": 0.6874571442604065,
            "normalized_value": "",
            "text_value": "08.04.25",
        },
        "header": {
            "confidence": 0.9993054866790771,
            "normalized_value": "",
            "text_value": "אינטרנט + TV",
        },
        "issued_for": {
            "confidence": 0.9994539618492126,
            "normalized_value": "",
            "text_value": "גולדין יבגני",
        },
        "pay_period": {
            "confidence": 0.9855984449386597,
            "normalized_value": "",
            "text_value": "2025 מאי",
        },
        "to_date": {
            "confidence": 0.990985631942749,
            "normalized_value": "",
            "text_value": "07.05.25",
        },
        "total_sum": {
            "confidence": 0.9978411793708801,
            "normalized_value": "",
            "text_value": "₪205.70",
        },
    }
    data = {k: v.get("text_value") for k, v in raw_data.items()}
    yield Invoice(**data)

@pytest.fixture
def group_id():
    yield os.getenv("SPLITWISE_GROUP_ID")

def test_create_expence(group_id, invoice):
    file_path = r'"C:\Users\goldi\Desktop\Billi-bot model set\training\cellcom\83c6a874-9210-11f0-abe0-5cbaef186814.jpg"'
    expense = create_expense(group_id, invoice, file_path)
    assert expense
    
def test_post_expence(group_id, invoice):
    file_path = r"C:\Users\goldi\Desktop\Billi-bot model set\training\cellcom\83c6a874-9210-11f0-abe0-5cbaef186814.jpg"
    expence = create_expense(group_id, invoice, file_path)
    _id = post_expense(expence)
    assert type(_id) is int
    assert _id != 0
    
def test_post_expence_unknown_group(invoice):
    expence = create_expense(9999, invoice)
    with pytest.raises(SplitwiseNotAllowedException):
        _id = post_expense(expence)
  
    
