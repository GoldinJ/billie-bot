from . import InvoiceType

class InvoiceClassifier:
    _classification_map = {
        InvoiceType.WATER: ['מים', 'ביוב', 5800],
        InvoiceType.ELECTRICITY: ['חברת החשמל', 'חשמל'],
        InvoiceType.GAS: ['גז', 'הספקת גז'],
        InvoiceType.INTERNET: ['אינטרנט', 'TV'],
        InvoiceType.PROPERTY_TAX: ['ארנונה'],
    }

    
    def classify(self, data: str | dict) -> InvoiceType:
        if isinstance(data, dict):
            return self._classify_dict(data)
        if isinstance(data, str):
            return self._classify_str(data)
        
        raise TypeError(f"Unsupported type for data argument: {type(data)}")
    
    def _classify_str(self, data: str) -> InvoiceType:
        for invoice_type, keywords in self._classification_map.items():
            if any(str(keyword) in data for keyword in keywords):
                return invoice_type
        return InvoiceType.UNSUPPORTED
    
    def _classify_dict(self, data: dict[str, dict]) -> InvoiceType:
        for value in data.values():
            _type = self._classify_str(str(value))
            if _type != InvoiceType.UNSUPPORTED:
                return _type
            
        return InvoiceType.UNSUPPORTED
        