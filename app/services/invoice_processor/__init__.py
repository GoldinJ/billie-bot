from enum import Enum

class InvoiceType(Enum):
    WATER = "water"
    ELECTRICITY = "electricity"
    GAS = "gas"
    INTERNET = "internet"
    PROPERTY_TAX = "property_tax"
    UNSUPPORTED = "unsupported"