from enum import Enum

class InvoiceType(Enum):
    WATER = 7
    ELECTRICITY = 5
    GAS = 6
    INTERNET = 8
    PROPERTY_TAX = 45 # Arnona
    UNSUPPORTED = 0