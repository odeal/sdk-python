from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketListResult:
    """
    Sepet listeleme sonucu.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    baskets: List['BasketSummary'] = field(default_factory=list)
    """"""
    total_pages: Optional[int] = None
    """"""
    total_elements: Optional[int] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketListResult']:
        if not data:
            return None
        # Nested Type: BasketSummary
        from .basket_summary import BasketSummary
        baskets_data = data.get("baskets")
        baskets = [deserialize(item, BasketSummary) for item in baskets_data] if baskets_data else []
        total_pages = data.get("totalPages")
        total_elements = data.get("totalElements")

        return cls(
            baskets=baskets,
            total_pages=total_pages,
            total_elements=total_elements,
        )
