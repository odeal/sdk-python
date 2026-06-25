from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketResponse:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    result: Optional['BasketCreateResult'] = None
    """Oluşturulan sepetin sonucu."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketResponse']:
        if not data:
            return None
        # Nested Type: BasketCreateResult
        from .basket_create_result import BasketCreateResult
        result_data = data.get("result")
        result = deserialize(result_data, BasketCreateResult)

        return cls(
            result=result,
        )
