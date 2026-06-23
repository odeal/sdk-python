from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketPrice:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "gross_price": {"required": True,
        },
    }
    gross_price: Optional[float] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketPrice']:
        if not data:
            return None
        # Nested Type: double
        from .double import double
        gross_price_data = data.get("grossPrice")
        gross_price = deserialize(gross_price_data, double)

        return cls(
            gross_price=gross_price,
        )
