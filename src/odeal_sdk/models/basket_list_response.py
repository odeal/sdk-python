from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketListResponse:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    result: Optional['BasketListResult'] = None
    """Sepet listeleme sonucu."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketListResponse']:
        if not data:
            return None
        # Nested Type: BasketListResult
        from .basket_list_result import BasketListResult
        result_data = data.get("result")
        result = deserialize(result_data, BasketListResult)

        return cls(
            result=result,
        )
