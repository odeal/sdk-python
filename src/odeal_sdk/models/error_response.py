from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ErrorResponse:
    """
    API iş kuralı hata yanıt modeli (BUSINESS hataları).
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    code: Optional[int] = None
    """İş kuralı hata kodu (ör. 2029)."""
    exception_type: Optional[str] = None
    """Hata tipi (ör. BUSINESS, VALIDATION)."""
    message: Optional[str] = None
    """Teknik hata açıklaması."""
    user_message: Optional[str] = None
    """Son kullanıcıya gösterilebilecek mesaj."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ErrorResponse']:
        if not data:
            return None
        code = data.get("code")
        exception_type = data.get("exceptionType")
        message = data.get("message")
        user_message = data.get("userMessage")

        return cls(
            code=code,
            exception_type=exception_type,
            message=message,
            user_message=user_message,
        )
