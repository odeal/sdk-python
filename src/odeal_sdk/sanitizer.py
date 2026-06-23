"""
Odeal SDK Sanitizer Modülü.

Hassas verileri maskeleyen yardımcı fonksiyonlar.
Interceptor body verileri ve debug loglarında hassas verilerin sızmasını engeller.
"""

import json as _json
import re
from typing import Any, Dict, Optional

_SENSITIVE_FIELDS = [
    "password", "cvv", "cvc", "cardNumber", "card_number", "pan",
    "expiryDate", "expiry_date", "securityCode", "security_code",
    "secretKey", "secret_key", "token", "accessToken", "access_token",
    "refreshToken", "refresh_token", "authorization",
    "tckn", "tcKimlikNo", "tcKimlik", "identityNumber", "nationalId",
    "iban", "phone", "phoneNumber", "telephone", "gsm",
    "email", "eMail", "mail", "address", "adres",
]

_SENSITIVE_HEADER_KEYWORDS = ["secret", "key", "authorization", "token", "cookie", "session"]

_SENSITIVE_FIELD_SET = {f.lower() for f in _SENSITIVE_FIELDS}


def sanitize_json(json_str: Optional[str]) -> Optional[str]:
    """JSON string içindeki hassas alanları maskeler.

    JSON ağacı parse edilerek iç içe nesneler, diziler ve string olmayan değerler
    (sayı, boolean) dahil tüm hassas alanlar maskelenir. Geçerli JSON değilse regex
    tabanlı güvenli yedeğe düşülür.
    """
    if not json_str:
        return json_str

    try:
        parsed = _json.loads(json_str)
    except (ValueError, TypeError):
        return _sanitize_json_regex(json_str)

    return _json.dumps(_mask_value(parsed), ensure_ascii=False, separators=(",", ":"))


def _mask_value(value: Any) -> Any:
    """JSON değerini recursive olarak gezerek hassas alanları maskeler."""
    if isinstance(value, dict):
        return {
            k: ("***" if str(k).lower() in _SENSITIVE_FIELD_SET else _mask_value(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_mask_value(v) for v in value]
    return value


def _sanitize_json_regex(json_str: str) -> str:
    """Parse edilemeyen içerik için regex tabanlı yedek maskeleme."""
    result = json_str
    for field in _SENSITIVE_FIELDS:
        pattern = rf'("{re.escape(field)}"\s*:\s*")[^"]*(")'
        result = re.sub(pattern, r"\1***\2", result, flags=re.IGNORECASE)
    return result


def sanitize_headers(headers: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Header dictionary'sindeki hassas değerleri maskeler."""
    if not headers:
        return {}

    sanitized = {}
    for key, value in headers.items():
        lower = key.lower()
        is_sensitive = any(kw in lower for kw in _SENSITIVE_HEADER_KEYWORDS)
        sanitized[key] = "***" if is_sensitive else value
    return sanitized
