from app.services.invoice_processor import InvoiceType
from app.services.invoice_processor.classifier import InvoiceClassifier


def test_classify_tv_interner():
    data = {
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
    invoice_type = InvoiceClassifier().classify(data)
    assert invoice_type == InvoiceType.INTERNET
    
def test_classify_water():
    data = {'invoice_id': {'confidence': 0.9233940243721008,
                'normalized_value': '',
                'text_value': '21039073'},
 'issued_for': {'confidence': 0.9983379244804382,
                'normalized_value': '',
                'text_value': 'גולדין יבגני'},
 'mislaka': {'confidence': 0.9955987930297852,
             'normalized_value': '',
             'text_value': '3193089030-1'},
 'pay_period': {'confidence': 0.9990437030792236,
                'normalized_value': '',
                'text_value': '63'},
 'pay_until': {'confidence': 0.9768437743186951,
               'normalized_value': '',
               'text_value': '30/09/25'},
 'property_address': {'confidence': 0.9998162984848022,
                      'normalized_value': '',
                      'text_value': 'שטרן יאיר 23'},
 'property_info': {'confidence': 0.9306913018226624,
                   'normalized_value': '',
                   'text_value': '5800'},
 'total_sum': {'confidence': 0.6499125361442566,
               'normalized_value': '',
               'text_value': '222.95 ₪'}}
    
    invoice_type = InvoiceClassifier().classify(data)
    assert invoice_type == InvoiceType.WATER
