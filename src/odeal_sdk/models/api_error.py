from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class ApiError:
    """
    Hata detaylari.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    code: Optional[int] = None
    """HTTP status kodu."""
    message: Optional[str] = None
    """Kullaniciya gosterilebilecek hata mesaji."""
    details: Optional[str] = None
    """Opsiyonel teknik detay."""
    timestamp: Optional[str] = None
    """Hatanin olustu zaman."""
    path: Optional[str] = None
    """Hatanin olustugu endpoint."""
    validation_errors: Optional[List['ValidationError']] = None
    """Validasyon hatalari (400 icin)."""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ApiError']:
        if not data:
            return None
        code = data.get("code")
        message = data.get("message")
        details = data.get("details")
        timestamp = data.get("timestamp")
        path = data.get("path")
        # Nested Type: ValidationError
        from .validation_error import ValidationError
        validation_errors_data = data.get("validationErrors")
        validation_errors = [deserialize(item, ValidationError) for item in validation_errors_data] if validation_errors_data else None

        return cls(
            code=code,
            message=message,
            details=details,
            timestamp=timestamp,
            path=path,
            validation_errors=validation_errors,
        )
