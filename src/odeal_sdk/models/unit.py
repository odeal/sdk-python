from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class Unit:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    id: Optional[int] = None
    """"""
    code: Optional[str] = None
    """"""
    name: Optional[str] = None
    """"""
    decimal: Optional[bool] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Unit']:
        if not data:
            return None
        id = data.get("id")
        code = data.get("code")
        name = data.get("name")
        decimal = data.get("decimal")

        return cls(
            id=id,
            code=code,
            name=name,
            decimal=decimal,
        )
