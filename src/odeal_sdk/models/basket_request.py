from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketRequest:
    """
    
    """
    
    _config_map = {
        "external_device_key": "external_device_key",
    }
    
    _validation_rules = {
        "reference_code": {"required": True,"pattern": r"^.{1,50}$", "message": "Referans kodu 1-50 karakter arasında olmalıdır."
        },
        "external_device_key": {"pattern": r"^.{1,}$", "message": "Cihaz kodu boş olamaz."
        },
        "customer": {"required": True,
        },
        "price": {"required": True,
        },
        "items": {"required": True,
        },
        "payment_options": {"required": True,
        },
    }
    reference_code: Optional[str] = None
    """"""
    external_device_key: Optional[str] = None
    """"""
    basket_type: Optional['BasketType'] = None
    """Default: SIMPLE"""
    receipt_info: Optional['ReceiptInfo'] = None
    """Opsiyonel."""
    customer: Optional['Customer'] = None
    """"""
    price: Optional['BasketPrice'] = None
    """"""
    items: Optional[List['Item']] = None
    """Zorunlu."""
    payment_options: Optional[List['PaymentOption']] = None
    """Zorunlu. Ödeme yöntemleri."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketRequest']:
        if not data:
            return None
        reference_code = data.get("referenceCode")
        external_device_key = data.get("externalDeviceKey")
        # Nested Type: BasketType
        from ..enums.basket_type import BasketType
        basket_type_raw = data.get("basketType")
        basket_type = BasketType(basket_type_raw) if basket_type_raw else None
        # Nested Type: ReceiptInfo
        from .receipt_info import ReceiptInfo
        receipt_info_data = data.get("receiptInfo")
        receipt_info = deserialize(receipt_info_data, ReceiptInfo)
        # Nested Type: Customer
        from .customer import Customer
        customer_data = data.get("customer")
        customer = deserialize(customer_data, Customer)
        # Nested Type: BasketPrice
        from .basket_price import BasketPrice
        price_data = data.get("price")
        price = deserialize(price_data, BasketPrice)
        # Nested Type: Item
        from .item import Item
        items_data = data.get("items")
        items = [deserialize(item, Item) for item in items_data] if items_data else None
        # Nested Type: PaymentOption
        from .payment_option import PaymentOption
        payment_options_data = data.get("paymentOptions")
        payment_options = [deserialize(item, PaymentOption) for item in payment_options_data] if payment_options_data else None

        return cls(
            reference_code=reference_code,
            external_device_key=external_device_key,
            basket_type=basket_type,
            receipt_info=receipt_info,
            customer=customer,
            price=price,
            items=items,
            payment_options=payment_options,
        )
