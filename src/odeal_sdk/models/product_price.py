from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ProductPrice:
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
    vat_ratio: Optional[int] = None
    """"""
    sct_ratio: Optional[int] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ProductPrice']:
        if not data:
            return None
        gross_price = data.get("grossPrice")
        vat_ratio = data.get("vatRatio")
        sct_ratio = data.get("sctRatio")

        return cls(
            gross_price=gross_price,
            vat_ratio=vat_ratio,
            sct_ratio=sct_ratio,
        )
