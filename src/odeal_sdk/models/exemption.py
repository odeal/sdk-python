from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class Exemption:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "code": {"pattern": r"^.{1,}$", "message": "Code formatı geçersiz."
        },
    }
    code: Optional[str] = None
    """"""
    description: Optional[str] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Exemption']:
        if not data:
            return None
        code = data.get("code")
        description = data.get("description")

        return cls(
            code=code,
            description=description,
        )
