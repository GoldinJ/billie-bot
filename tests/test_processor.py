from app.services.invoice_processor.proccessor import InvoiceProcessor
from app.services.invoice_processor import InvoiceType

def test_process_document_image():
    file_path = r'C:\Users\goldi\Documents\PythonProjects\billie-bot\media\30a78570-954f-11f0-a17a-5cbaef186814.jpg'
    invoice = InvoiceProcessor(file_path).process_invoice()
    assert len(invoice) == 3
    assert invoice[0] == InvoiceType.PROPERTY_TAX
    assert invoice[1] == "Property Tax - 9/2025"
    assert invoice[2] == 704.84