from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class TransactionReport:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    basket_reference_code: Optional[str] = None
    """"""
    payment_id: Optional[str] = None
    """"""
    current_status: Optional[str] = None
    """"""
    amount: Optional[str] = None
    """"""
    invoice_number: Optional[str] = None
    """"""
    invoice_pdf_url: Optional[str] = None
    """"""
    basket_status: Optional[str] = None
    """"""
    invoice_gib_status_code: Optional[int] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['TransactionReport']:
        if not data:
            return None
        basket_reference_code = data.get("basketReferenceCode")
        payment_id = data.get("paymentId")
        current_status = data.get("currentStatus")
        amount = data.get("amount")
        invoice_number = data.get("invoiceNumber")
        invoice_pdf_url = data.get("invoicePdfUrl")
        basket_status = data.get("basketStatus")
        invoice_gib_status_code = data.get("invoiceGibStatusCode")

        return cls(
            basket_reference_code=basket_reference_code,
            payment_id=payment_id,
            current_status=current_status,
            amount=amount,
            invoice_number=invoice_number,
            invoice_pdf_url=invoice_pdf_url,
            basket_status=basket_status,
            invoice_gib_status_code=invoice_gib_status_code,
        )
