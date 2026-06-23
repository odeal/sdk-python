from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ReceiptInfo:
    """
    Fiş detayları. Tüm sepet tipleri için ortak yapıdır.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "receipt_number": {"pattern": r"^.{1,50}$", "message": "ReceiptNumber formatı geçersiz."
        },
        "receipt_date": {"pattern": r"^\d{4}-\d{2}-\d{2}$", "message": "Fiş tarihi YYYY-MM-DD formatında olmalıdır."
        },
        "siparis_no": {"pattern": r"^.{0,50}$", "message": "SiparisNo formatı geçersiz."
        },
        "garson": {"pattern": r"^.{0,50}$", "message": "Garson formatı geçersiz."
        },
    }
    food_card_brand_id: Optional['ReceiptInfoFoodCardBrandId'] = None
    """Koşullu. Eğer ödeme tipi 'FOOD_CARD' ise ZORUNLUDUR.
    /// - 100001: Multinet
    /// - 100002: Setcard
    /// - 100003: Edenred
    /// - 100004: Tokenflex
    /// - 100005: Pluxee
    /// - 100006: Metropol
    /// - 100007: Paye"""
    receipt_number: Optional[str] = None
    """Koşullu. Sadece 'CURRENT_ACCOUNT' (Cari Hesap) işleminde kullanılır (Fatura/Ekstre No)."""
    receipt_date: Optional[str] = None
    """Koşullu. Sadece 'CURRENT_ACCOUNT' (Cari Hesap) işleminde kullanılır (YYYY-MM-DD)."""
    siparis_no: Optional[str] = None
    """Opsiyonel."""
    garson: Optional[str] = None
    """Opsiyonel."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ReceiptInfo']:
        if not data:
            return None
        # Nested Type: ReceiptInfoFoodCardBrandId
        from ..enums.receipt_info_food_card_brand_id import ReceiptInfoFoodCardBrandId
        food_card_brand_id_raw = data.get("foodCardBrandId")
        food_card_brand_id = ReceiptInfoFoodCardBrandId(food_card_brand_id_raw) if food_card_brand_id_raw else None
        receipt_number = data.get("receiptNumber")
        receipt_date = data.get("receiptDate")
        siparis_no = data.get("SiparisNo")
        garson = data.get("Garson")

        return cls(
            food_card_brand_id=food_card_brand_id,
            receipt_number=receipt_number,
            receipt_date=receipt_date,
            siparis_no=siparis_no,
            garson=garson,
        )
