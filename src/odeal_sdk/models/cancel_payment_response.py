from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class CancelPaymentResponse:
    """
    Ödeme iptal yanıtı.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    result: Optional['CancelPaymentResult'] = None
    """Ödeme iptal sonucu."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['CancelPaymentResponse']:
        if not data:
            return None
        # Nested Type: CancelPaymentResult
        from .cancel_payment_result import CancelPaymentResult
        result_data = data.get("result")
        result = deserialize(result_data, CancelPaymentResult)

        return cls(
            result=result,
        )
