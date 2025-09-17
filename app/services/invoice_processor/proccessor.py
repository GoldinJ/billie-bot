from os import getenv
from ..google.google_utils import process_document

class InvoiceProcessor:
    project_id = getenv("GOOGLE_PROJECT_ID")
    location = getenv("GOOGLE_PROCESSOR_REGION")
    processor_id = getenv("GOOGLE_PROCESSOR_ID")
    processor_version_id = getenv("GOOGLE_PROCESSOR_VERSION_ID")
    
    @classmethod
    def process_invoice(cls, file_path: str) -> dict:
        document = process_document(
            file_path=file_path,
            project_id=cls.project_id,
            location=cls.location,
            processor_id=cls.processor_id,
            processor_version_id=cls.processor_version_id
        )
        return document
