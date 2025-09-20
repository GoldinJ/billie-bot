from os import getenv, path
import logging
from ..google.google_utils import process_document
from .invoice import Invoice


class InvoiceProcessor:
    project_id = getenv("GOOGLE_PROJECT_ID")
    location = getenv("GOOGLE_PROCESSOR_REGION")
    processor_id = getenv("GOOGLE_PROCESSOR_ID")
    processor_version_id = getenv("GOOGLE_PROCESSOR_VERSION_ID")
    
    def __init__(self, file_path: str):
        self._invoice = None
        self._file_path = file_path
        
    @property
    def invoice(self):
        if self._invoice is None:
            self._invoice = self._get_invoice()
            
        return self._invoice
    
    def _get_invoice(self) -> Invoice | None:
        if not path.isfile(self._file_path):
            logging.debug(f'{self._file_path} - not a file')
            return None
        
        fields, text  = process_document(
            file_path=self._file_path,
            project_id=self.project_id,
            location=self.location,
            processor_id=self.processor_id,
            processor_version_id=self.processor_version_id,
        )
        invoice = Invoice(**{k: v.get('text_value') for k, v in fields.items()}, text=text)
        
        return invoice

    def process_invoice(self):
        return self.invoice