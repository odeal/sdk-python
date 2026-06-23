from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ConfigurationResponse:
    """
    Konfigürasyon bilgisi.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    ecommerce_url: Optional[str] = None
    """"""
    basket_url: Optional[str] = None
    """"""
    payment_succeeded_url: Optional[str] = None
    """"""
    payment_cancelled_url: Optional[str] = None
    """"""
    payment_failed_url: Optional[str] = None
    """"""
    einvoice_created_url: Optional[str] = None
    """"""
    einvoice_cancelled_url: Optional[str] = None
    """"""
    callback_payout_url: Optional[str] = None
    """"""
    basket_cancelled_url: Optional[str] = None
    """"""
    basket_process_failed_url: Optional[str] = None
    """"""
    einvoice_integrator: Optional[str] = None
    """"""
    basket_type: Optional[str] = None
    """"""
    odeal_request_key: Optional[str] = None
    """"""
    customer_get_url: Optional[str] = None
    """"""
    customer_post_url: Optional[str] = None
    """"""
    customer_put_url: Optional[str] = None
    """"""
    intent_url: Optional[str] = None
    """"""
    app_name: Optional[str] = None
    """"""
    close_after_payment: Optional[bool] = None
    """"""
    authorization_type: Optional[str] = None
    """"""
    basic_auth_username: Optional[str] = None
    """"""
    basic_auth_password: Optional[str] = None
    """"""
    terminal_id: Optional[str] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ConfigurationResponse']:
        if not data:
            return None
        ecommerce_url = data.get("ecommerceUrl")
        basket_url = data.get("basketUrl")
        payment_succeeded_url = data.get("paymentSucceededUrl")
        payment_cancelled_url = data.get("paymentCancelledUrl")
        payment_failed_url = data.get("paymentFailedUrl")
        einvoice_created_url = data.get("einvoiceCreatedUrl")
        einvoice_cancelled_url = data.get("einvoiceCancelledUrl")
        callback_payout_url = data.get("callbackPayoutUrl")
        basket_cancelled_url = data.get("basketCancelledUrl")
        basket_process_failed_url = data.get("basketProcessFailedUrl")
        einvoice_integrator = data.get("einvoiceIntegrator")
        basket_type = data.get("basketType")
        odeal_request_key = data.get("odealRequestKey")
        customer_get_url = data.get("customerGetUrl")
        customer_post_url = data.get("customerPostUrl")
        customer_put_url = data.get("customerPutUrl")
        intent_url = data.get("intentUrl")
        app_name = data.get("appName")
        close_after_payment = data.get("closeAfterPayment")
        authorization_type = data.get("authorizationType")
        basic_auth_username = data.get("basicAuthUsername")
        basic_auth_password = data.get("basicAuthPassword")
        terminal_id = data.get("terminalId")

        return cls(
            ecommerce_url=ecommerce_url,
            basket_url=basket_url,
            payment_succeeded_url=payment_succeeded_url,
            payment_cancelled_url=payment_cancelled_url,
            payment_failed_url=payment_failed_url,
            einvoice_created_url=einvoice_created_url,
            einvoice_cancelled_url=einvoice_cancelled_url,
            callback_payout_url=callback_payout_url,
            basket_cancelled_url=basket_cancelled_url,
            basket_process_failed_url=basket_process_failed_url,
            einvoice_integrator=einvoice_integrator,
            basket_type=basket_type,
            odeal_request_key=odeal_request_key,
            customer_get_url=customer_get_url,
            customer_post_url=customer_post_url,
            customer_put_url=customer_put_url,
            intent_url=intent_url,
            app_name=app_name,
            close_after_payment=close_after_payment,
            authorization_type=authorization_type,
            basic_auth_username=basic_auth_username,
            basic_auth_password=basic_auth_password,
            terminal_id=terminal_id,
        )
