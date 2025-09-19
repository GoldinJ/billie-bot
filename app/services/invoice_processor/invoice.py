import re
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from .classifier import InvoiceClassifier, InvoiceType

@dataclass
class Invoice:
    """
    A dataclass to represent an Invoice.

    All fields are optional and default to None.

    Attributes:
        from_date (Optional[str]): The starting date of the invoice period.
        header (Optional[str]): The header or title of the invoice.
        invoice_id (Optional[str]): A unique identifier for the invoice.
        invoice_num (Optional[str]): The invoice number.
        issued_for (Optional[str]): The person or entity the invoice was issued for.
        last_date (Optional[str]): The end date of the invoice period.
        mislaka (Optional[str]): A field for 'mislaka' data.
        pay_period (Optional[str]): The period for which the payment is due.
        pay_until (Optional[str]): The due date for the payment.
        property_address (Optional[str]): The address of the property related to the invoice.
        property_info (Optional[str]): Additional information about the property.
        to_date (Optional[str]): The end date of the invoice period.
        total_sum (Optional[float]): The total sum of the invoice. It is sanitized upon initialization.
    """
    from_date: Optional[str] = None
    header: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_num: Optional[str] = None
    issued_for: Optional[str] = None
    last_date: Optional[str] = None
    mislaka: Optional[str] = None
    pay_period: Optional[str] = None
    pay_until: Optional[str] = None
    property_address: Optional[str] = None
    property_info: Optional[str] = None
    to_date: Optional[str] = None
    total_sum: Optional[float] = None
    text: Optional[float] = None
                
    @property
    def invoice_type(self) -> InvoiceType:
        return InvoiceClassifier().classify(vars(self))
    
    @property
    def cost(self) -> float:
        if not self.total_sum:
            return 0.0
        
        match = re.findall("\d+", self.total_sum)
        
        if not match:
            return 0.0
        elif len(match) == 1:
            return float(match[0])
        elif len(match) >= 2:
            return float(f'{match[0]}.{match[1]}')
        
        return 0.0
        
    @property
    def description(self):
        timestamp = datetime.now()
        title = f"{self.invoice_type.name.title().replace("_", " ")} - {timestamp.month}/{timestamp.year}"
        return title
    
    def get_summary(self):
        return (
            self.invoice_type,
            self.description,
            self.cost
            )