from pytest import raises
from services.google.google_utils import get_mime_type
from services.google import GoogleFileType

def test_get_mime_type():
    assert get_mime_type("document.pdf") == GoogleFileType.PDF
    assert get_mime_type("image.png") == GoogleFileType.PNG
    assert get_mime_type("image.jpeg") == GoogleFileType.JPEG
    assert get_mime_type("image.jpg") == GoogleFileType.JPG
    
def test_get_mime_type_case_insensitive():
    assert get_mime_type("document.PDF") == GoogleFileType.PDF
    assert get_mime_type("image.PNG") == GoogleFileType.PNG
    assert get_mime_type("image.JPEG") == GoogleFileType.JPEG
    assert get_mime_type("image.JPG") == GoogleFileType.JPG
    
def test_get_mime_type_no_extension():
    assert get_mime_type("file") is None