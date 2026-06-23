from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ConfigurationRequest:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    e_commerce_url: Optional[str] = None
    """"""
    basket_url: Optional[str] = None
    """Sepet bilgisinin alınacağı URL (external-basket için)."""
    payment_succeeded_url: Optional[str] = None
    """Ödeme başarılı bildirimi için URL."""
    payment_failed_url: Optional[str] = None
    """Ödeme başarısız bildirimi için URL."""
    payment_cancelled_url: Optional[str] = None
    """İptal bildirimi için URL."""
    e_invoice_created_url: Optional[str] = None
    """"""
    e_invoice_integrator: Optional[str] = None
    """"""
    odeal_request_key: Optional[str] = None
    """Webhook isteklerinde güvenlik için X-ODEAL-REQUEST-KEY olarak gönderilir."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConfigurationRequest']:
        if not data:
            return None
        e_commerce_url = data.get("eCommerceUrl")
        basket_url = data.get("basketUrl")
        payment_succeeded_url = data.get("paymentSucceededUrl")
        payment_failed_url = data.get("paymentFailedUrl")
        payment_cancelled_url = data.get("paymentCancelledUrl")
        e_invoice_created_url = data.get("eInvoiceCreatedUrl")
        e_invoice_integrator = data.get("eInvoiceIntegrator")
        odeal_request_key = data.get("odealRequestKey")

        return cls(
            e_commerce_url=e_commerce_url,
            basket_url=basket_url,
            payment_succeeded_url=payment_succeeded_url,
            payment_failed_url=payment_failed_url,
            payment_cancelled_url=payment_cancelled_url,
            e_invoice_created_url=e_invoice_created_url,
            e_invoice_integrator=e_invoice_integrator,
            odeal_request_key=odeal_request_key,
        )
