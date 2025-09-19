import os
import pytest
from splitwise.exception import SplitwiseNotAllowedException
from app.services.invoice_processor.invoice import Invoice
from app.services.splitwise.spitwise_utils import (
    create_expense,
    post_expence
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
    expense = create_expense(group_id, invoice)
    assert expense
    
def test_post_expence(group_id, invoice):
    expence = create_expense(group_id, invoice)
    _id = post_expence(expence)
    assert type(_id) is int
    assert _id != 0
    
def test_post_expence_unknown_group(invoice):
    expence = create_expense(9999, invoice)
    with pytest.raises(SplitwiseNotAllowedException):
        _id = post_expence(expence)
  
    
