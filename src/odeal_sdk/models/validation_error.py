from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ValidationError:
    """
    Tek bir alan icin validasyon hatasi.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    field: Optional[str] = None
    """Hatali alanin adi."""
    message: Optional[str] = None
    """Validasyon hata mesaji."""
    rejected_value: Optional[str] = None
    """Reddedilen deger."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ValidationError']:
        if not data:
            return None
        field = data.get("field")
        message = data.get("message")
        rejected_value = data.get("rejectedValue")

        return cls(
            field=field,
            message=message,
            rejected_value=rejected_value,
        )
