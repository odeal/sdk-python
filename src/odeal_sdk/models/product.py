from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class Product:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "unit_code": {"required": True,
        },
        "name": {"required": True,"pattern": r"^.{1,255}$", "message": "Ürün adı 1-255 karakter arasında olmalıdır."
        },
        "reference_code": {"required": True,"pattern": r"^.{1,50}$", "message": "Ürün kodu 1-50 karakter arasında olmalıdır."
        },
        "price": {"required": True,
        },
    }
    unit_code: Optional['ProductUnitCode'] = None
    """Birim Kodları.
    /// - _3I: Kilogram-Adet (C# Uyumu için ön ekli)"""
    name: Optional[str] = None
    """"""
    reference_code: Optional[str] = None
    """"""
    price: Optional['ProductPrice'] = None
    """"""
    exemption: Optional['Exemption'] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Product']:
        if not data:
            return None
        # Nested Type: ProductUnitCode
        from ..enums.product_unit_code import ProductUnitCode
        unit_code_raw = data.get("unitCode")
        unit_code = ProductUnitCode(unit_code_raw) if unit_code_raw else None
        name = data.get("name")
        reference_code = data.get("referenceCode")
        # Nested Type: ProductPrice
        from .product_price import ProductPrice
        price_data = data.get("price")
        price = deserialize(price_data, ProductPrice)
        # Nested Type: Exemption
        from .exemption import Exemption
        exemption_data = data.get("exemption")
        exemption = deserialize(exemption_data, Exemption)

        return cls(
            unit_code=unit_code,
            name=name,
            reference_code=reference_code,
            price=price,
            exemption=exemption,
        )
