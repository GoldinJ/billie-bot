from enum import Enum


class GoogleFileType(Enum):
    PDF = "application/pdf"
    PNG = "image/png"
    JPEG = "image/jpeg"
    JPG = "image/jpeg"
    
    @classmethod
    def get_mime_type(cls, file:str) -> 'GoogleFileType':
        try:
            ext = file.split('.')[-1].upper()
            return cls[ext]
        except KeyError:
            raise ValueError(f"Unsupported file type: {file}")