import os
import logging
from typing import Optional, Literal
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

from . import GoogleFileType

def get_mime_type(file: str) -> 'GoogleFileType':
    try:
        return GoogleFileType.get_mime_type(file)
    except ValueError as e:
        logging.error(e)
        return None

def layout_to_text(layout: documentai.Document.Page.Layout, text: str) -> str:
    """
    Document AI identifies text in different parts of the document by their
    offsets in the entirety of the document"s text. This function converts
    offsets to a string.
    """
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    return "".join(
        text[int(segment.start_index) : int(segment.end_index)]
        for segment in layout.text_anchor.text_segments
    )

def process_document(file_path: str,
                     project_id: str,
                     location: Literal["us", "eu"],
                     processor_id: str,
                     processor_version_id: Optional[str] = None,
                     field_mask: Optional[str] = None) -> documentai.Document:
    """
    Processes a document using Google Cloud Document AI.

    Args:
        file_path (str): The path to the document file to be processed.
        project_id (str): The GCP project ID.
        location (str): The location of the processor (e.g., "us" or "eu").
        processor_id (str): The ID of the processor to use.
        processor_version_id (Optional[str]): The version ID of the processor (if applicable).
        field_mask (Optional[str]): The field mask to specify which fields to include in the response.
    """
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)
    ext = GoogleFileType.get_mime_type(file_path)
    process_options = documentai.ProcessOptions()

    if not os.path.isfile(file_path):
        logging.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not ext:
        raise ValueError(f"Unsupported file type for file: {file_path}")
    elif ext == GoogleFileType.PDF:
        page_selector=documentai.ProcessOptions.IndividualPageSelector(pages=[1])
        process_options = documentai.ProcessOptions(
            individual_page_selector=page_selector
        )
        

    if processor_version_id:
        # The full resource name of the processor version, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
        name = client.processor_version_path(
            project_id, location, processor_id, processor_version_id
        )
    else:
        # The full resource name of the processor, e.g.:
        # `projects/{project_id}/locations/{location}/processors/{processor_id}`
        name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(content=image_content, mime_type=ext.value)

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document,
        field_mask=field_mask,
        process_options=process_options
    )

    response = client.process_document(request=request)
    return response.document

def process_document_form_sample(document: documentai.Document):
    # Read the table and form fields output from the processor
    # The form processor also contains OCR data. For more information
    # on how to parse OCR data please see the OCR sample.

    text = document.text
    form = {}
    for page in document.pages:
        for field in page.form_fields:
            name = layout_to_text(field.field_name, text)
            value = layout_to_text(field.field_value, text)
            form[name] = value

    return {k: str(v).strip() for k, v in form.items()}

