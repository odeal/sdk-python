from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class CancelPaymentResult:
    """
    Ödeme iptal sonucu.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    basket_reference_code: Optional[str] = None
    """"""
    message: Optional[str] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['CancelPaymentResult']:
        if not data:
            return None
        basket_reference_code = data.get("basketReferenceCode")
        message = data.get("message")

        return cls(
            basket_reference_code=basket_reference_code,
            message=message,
        )
