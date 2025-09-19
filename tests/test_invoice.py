import pytest
from app.services.invoice_processor.invoice import Invoice

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
@pytest.fixture
def data():
    data = {k: v.get('text_value', "") for k, v in raw_data.items()}
    yield data
    
@pytest.fixture
def text():
    text = ",".join(v.get("text_value", "") for v in raw_data.values())
    yield text


def test_invoice_init(data, text):
    invoice = Invoice(**data, text=text)
    assert invoice
    
def test_cost(data):
    invoice = Invoice(**data)
    assert invoice.cost == 205.70
    
def test_missing_sum(data):
    data.pop("total_sum", None)
    invoice = Invoice(**data)
    assert invoice.cost == 0.0
    
def test_invalid_sum(data):
    data['total_sum'] = "1.1.1"
    invoice = Invoice(**data)
    assert invoice.cost == 1.1
    
def test_text_instaed_sum(data):
    data['total_sum'] = "invalid"
    invoice = Invoice(**data)
    assert invoice.cost == 0.0
    
def test_description_no_header(data, text):
    data.pop("header", None)
    invoice = Invoice(**data, text=text)
    assert invoice.description == "Internet - 9/2025"
    
    
def test_description():
    pass

