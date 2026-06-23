"""
OdealConfig fluent builder.

Example:
    >>> config = (OdealConfigBuilder()
    ...     .secret_key('sk_xxx')
    ...     .merchant_key('mk_xxx')
    ...     .base_url('https://api.odeal.com/v1')
    ...     .debug_mode(True)
    ...     .timeout(60)
    ...     .max_retry_count(5)
    ...     .build())
"""

from .odeal_config import OdealConfig


class OdealConfigBuilder:
    """OdealConfig için fluent builder sınıfı."""
    
    def __init__(self):
        self._secret_key = None
        self._merchant_key = None
        self._base_url = 'https://api.odeal.com/v1'
        self._external_device_key = None
        self._skip_client_validation = False
        self._debug_mode = False
        self._timeout = 30
        self._max_retry_count = 3
        self._mask_sensitive_data = True
        self._interceptors = []
        self._logger = None

    def secret_key(self, secret_key: str) -> 'OdealConfigBuilder':
        self._secret_key = secret_key
        return self

    def merchant_key(self, merchant_key: str) -> 'OdealConfigBuilder':
        self._merchant_key = merchant_key
        return self

    def base_url(self, base_url: str) -> 'OdealConfigBuilder':
        self._base_url = base_url
        return self

    def environment(self, env) -> 'OdealConfigBuilder':
        """Ortam preset'i (OdealEnvironment.STAGING veya .PRODUCTION). base_url'i otomatik ayarlar."""
        self._base_url = env.get_base_url()
        return self

    def sandbox_mode(self, sandbox: bool = True) -> 'OdealConfigBuilder':
        """Sandbox (test) modu. Aktifken her zaman staging ortamı kullanılır."""
        if sandbox:
            from .odeal_environment import OdealEnvironment
            self._base_url = OdealEnvironment.STAGING.get_base_url()
        return self

    def external_device_key(self, key: str) -> 'OdealConfigBuilder':
        self._external_device_key = key
        return self

    def skip_client_validation(self, skip: bool = True) -> 'OdealConfigBuilder':
        self._skip_client_validation = skip
        return self

    def debug_mode(self, debug: bool = True) -> 'OdealConfigBuilder':
        self._debug_mode = debug
        return self

    def timeout(self, timeout: int) -> 'OdealConfigBuilder':
        self._timeout = timeout
        return self

    def max_retry_count(self, count: int) -> 'OdealConfigBuilder':
        self._max_retry_count = count
        return self

    def mask_sensitive_data(self, mask: bool = True) -> 'OdealConfigBuilder':
        self._mask_sensitive_data = mask
        return self

    def add_interceptor(self, interceptor) -> 'OdealConfigBuilder':
        self._interceptors.append(interceptor)
        return self

    def logger(self, logger) -> 'OdealConfigBuilder':
        self._logger = logger
        return self

    def build(self) -> OdealConfig:
        """OdealConfig'i oluşturur ve zorunlu alanları doğrular."""
        if not self._secret_key:
            raise ValueError("secret_key is required. Call .secret_key() before .build().")
        if not self._merchant_key:
            raise ValueError("merchant_key is required. Call .merchant_key() before .build().")

        config = OdealConfig(
            secret_key=self._secret_key,
            merchant_key=self._merchant_key,
            base_url=self._base_url,
            external_device_key=self._external_device_key,
            skip_client_validation=self._skip_client_validation,
            debug_mode=self._debug_mode,
            timeout=self._timeout,
            max_retry_count=self._max_retry_count,
            mask_sensitive_data=self._mask_sensitive_data,
            interceptors=self._interceptors or None,
            logger=self._logger,
        )
        return config
