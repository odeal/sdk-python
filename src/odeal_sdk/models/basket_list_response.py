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
    result: Optional[Any] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketListResponse']:
        if not data:
            return None
        result = data.get("result")

        return cls(
            result=result,
        )
