from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class Item:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "quantity": {"required": True,
        },
        "product": {"required": True,
        },
    }
    quantity: Optional[int] = None
    """"""
    product: Optional['Product'] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Item']:
        if not data:
            return None
        quantity = data.get("quantity")
        # Nested Type: Product
        from .product import Product
        product_data = data.get("product")
        product = deserialize(product_data, Product)

        return cls(
            quantity=quantity,
            product=product,
        )
