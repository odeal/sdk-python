from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class CancelPaymentRequest:
    """
    Ödeme iptal isteği.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "basket_reference_code": {"required": True,"pattern": r"^.{1,50}$", "message": "Referans kodu 1-50 karakter arasında olmalıdır."
        },
    }
    basket_reference_code: Optional[str] = None
    """İptal edilecek sepetin referans kodu"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['CancelPaymentRequest']:
        if not data:
            return None
        basket_reference_code = data.get("basketReferenceCode")

        return cls(
            basket_reference_code=basket_reference_code,
        )
