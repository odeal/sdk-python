from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class PaymentOption:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "amount": {"required": True,
        },
        "type": {"required": True,
        },
    }
    amount: Optional[float] = None
    """"""
    type: Optional['PaymentOptionType'] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['PaymentOption']:
        if not data:
            return None
        # Nested Type: double
        from .double import double
        amount_data = data.get("amount")
        amount = deserialize(amount_data, double)
        # Nested Type: PaymentOptionType
        from ..enums.payment_option_type import PaymentOptionType
        type_raw = data.get("type")
        type = PaymentOptionType(type_raw) if type_raw else None

        return cls(
            amount=amount,
            type=type,
        )
