from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketCreateResult:
    """
    Oluşturulan sepetin sonucu.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    id: Optional[int] = None
    """Oluşturulan sepetin kimliği."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketCreateResult']:
        if not data:
            return None
        id = data.get("id")

        return cls(
            id=id,
        )
