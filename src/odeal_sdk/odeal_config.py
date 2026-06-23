"""
Odeal SDK Konfigürasyon Modülü.

Bu modül, SDK'nın çalışması için gerekli yapılandırma ayarlarını içerir.

Example:
    >>> from odeal_sdk import OdealConfig
    >>> config = OdealConfig(
    ...     base_url="https://api.odeal.com/v1",
    ...     secret_key="your-secret-key",
    ...     merchant_key="your-merchant-key"
    ... )
"""

from dataclasses import dataclass, field
from typing import Optional
import logging


@dataclass
class OdealConfig:
    """
    SDK Konfigürasyon Ayarları.
    
    Attributes:
        base_url: API base URL'i. Varsayılan olarak production ortamı kullanılır.
        secret_key: API gizli anahtarı. Tüm isteklerde kimlik doğrulama için kullanılır.
        merchant_key: Üye iş yeri anahtarı.
        external_device_key: Harici cihaz anahtarı. POS cihazı tanımlama için kullanılır.
        skip_client_validation: İstemci tarafı validasyonunu atla. True olduğunda,
            SDK model üzerindeki validasyon kurallarını kontrol etmez.
        debug_mode: Hata ayıklama modu. Aktifken detaylı log çıktısı üretilir.
    
    Example:
        >>> config = OdealConfig(
        ...     base_url="https://api.odeal.com/v1",
        ...     secret_key="your-secret-key",
        ...     merchant_key="your-merchant-key",
        ...     skip_client_validation=False,
        ...     debug_mode=True
        ... )
    """
    base_url: str = "https://api.odeal.com/v1"
    secret_key: Optional[str] = None
    merchant_key: Optional[str] = None
    access_token: Optional[str] = None  # OAuth2/Bearer: ayarlıysa Authorization: Bearer eklenir
    external_device_key: Optional[str] = None
    skip_client_validation: bool = False
    debug_mode: bool = False
    
    # --- ENTERPRISE YETENEKLERİ ---
    
    # İstek zaman aşımı süresi (saniye cinsinden). Varsayılan 30 saniye.
    timeout: int = 30
    
    # Ağ veya 5xx sunucu hatalarında maksimum tekrar deneme sayısı.
    max_retry_count: int = 3
    
    # Loglama sırasında hassas verilerin gizlenmesini sağlar.
    mask_sensitive_data: bool = True
    
    # --- CIRCUIT BREAKER ---
    circuit_breaker_enabled: bool = False
    circuit_breaker_threshold: int = 5
    circuit_breaker_reset_ms: int = 60000
    
    # Özel loglama nesnesi (logging.Logger vb.). Belirtilmezse varsayılan logger kullanılır.
    logger: Optional['logging.Logger'] = None
    
    # HTTP istek/yanıt pipeline'ına araya girmek için interceptor listesi.
    interceptors: Optional[list] = None
    
    # Sandbox (test) modu. True olduğunda base_url değerine bakılmaksızın staging ortamı kullanılır.
    sandbox_mode: bool = False
    
    @property
    def effective_base_url(self) -> str:
        """Efektif base URL — sandbox_mode aktifse staging, değilse base_url döner."""
        if self.sandbox_mode:
            from .odeal_environment import OdealEnvironment
            return OdealEnvironment.STAGING.get_base_url()
        return self.base_url

    def __repr__(self) -> str:
        """Config'in okunabilir string temsilini döner (hassas veriler maskelenir)."""
        return (
            f"OdealConfig("
            f"base_url='{self.base_url}', "
            f"secret_key='{self._mask_secret(self.secret_key)}', "
            f"merchant_key='{self._mask_secret(self.merchant_key)}', "
            f"skip_client_validation={self.skip_client_validation}, "
            f"debug_mode={self.debug_mode}, "
            f"timeout={self.timeout}, "
            f"max_retry_count={self.max_retry_count}, "
            f"mask_sensitive_data={self.mask_sensitive_data})"
        )

    @staticmethod
    def _mask_secret(secret: Optional[str]) -> str:
        """Secret değerini maskeler: ilk 4 ve son 4 karakter görünür, arada '***'."""
        if not secret:
            return "(empty)"
        if len(secret) <= 8:
            return "***"
        return f"{secret[:4]}***{secret[-4:]}"
