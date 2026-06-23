"""
Odeal SDK Exception Modülü.

Bu modül, SDK tarafından fırlatılan tüm exception sınıflarını içerir.

Example:
    >>> try:
    ...     response = client.create_basket(request)
    ... except OdealRateLimitException as e:
    ...     print(f"Rate limit! {e.retry_after_seconds}s bekleyin.")
    ... except OdealAuthenticationException:
    ...     print("Geçersiz API anahtarı!")
    ... except OdealApiException as e:
    ...     print(f"API Hatası: {e.status_code} - {e.message}")
    ... except OdealValidationException as e:
    ...     print(f"Validation Hatası: {e.errors}")
"""

from typing import List, Optional


# ─── Base Exception ──────────────────────────────────────────

class OdealException(Exception):
    """Odeal SDK'dan fırlatılan tüm exception'ların temel sınıfı."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# ─── API Exceptions ──────────────────────────────────────────

class OdealApiException(OdealException):
    """
    API çağrılarında oluşan hataları temsil eder.
    
    Attributes:
        message: Hata mesajı.
        status_code: HTTP durum kodu.
        response_content: API'den dönen ham yanıt içeriği.
    """
    
    def __init__(self, message: str, status_code: int, response_content: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_content = response_content

    def __str__(self) -> str:
        return f"Status: {self.status_code}, Message: {self.message}, Content: {self.response_content}"
    
    def __repr__(self) -> str:
        return f"OdealApiException(message='{self.message}', status_code={self.status_code})"


class OdealAuthenticationException(OdealApiException):
    """Kimlik doğrulama hatası (HTTP 401 Unauthorized)."""
    
    def __init__(self, message: str = "Authentication failed. Please check your API keys.", response_content: Optional[str] = None):
        super().__init__(message, 401, response_content)


class OdealForbiddenException(OdealApiException):
    """Yetkilendirme hatası (HTTP 403 Forbidden)."""
    
    def __init__(self, message: str = "Access denied. You do not have permission for this operation.", response_content: Optional[str] = None):
        super().__init__(message, 403, response_content)


class OdealNotFoundException(OdealApiException):
    """Kaynak bulunamadı hatası (HTTP 404 Not Found)."""
    
    def __init__(self, message: str = "The requested resource was not found.", response_content: Optional[str] = None):
        super().__init__(message, 404, response_content)


class OdealRateLimitException(OdealApiException):
    """İstek limiti aşıldı hatası (HTTP 429 Too Many Requests)."""
    
    def __init__(self, message: str = "Rate limit exceeded. Please retry later.", response_content: Optional[str] = None, retry_after_seconds: Optional[int] = None):
        super().__init__(message, 429, response_content)
        self.retry_after_seconds = retry_after_seconds


# ─── Validation Exception ────────────────────────────────────

class OdealValidationException(OdealException):
    """Client-side validation hatalarını temsil eder."""
    
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or []

    def __str__(self) -> str:
        if self.errors:
            return f"Validation Error: {'; '.join(self.errors)}"
        return f"Validation Error: {self.message}"
    
    def __repr__(self) -> str:
        return f"OdealValidationException(message='{self.message}', errors={self.errors})"


# ─── Network Exceptions ──────────────────────────────────────

class OdealNetworkException(OdealException):
    """Ağ bağlantı hatası (DNS, bağlantı reddedildi vb.)."""
    
    def __init__(self, message: str):
        super().__init__(message)


class OdealTimeoutException(OdealNetworkException):
    """İstek zaman aşımı hatası."""
    
    def __init__(self, message: str = "The request timed out."):
        super().__init__(message)