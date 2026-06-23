"""
Odeal SDK Request Logger Middleware.

Interceptor pipeline üzerine inşa edilmiş, production-ready request/response logger.

Örnek kullanım:
    from odeal_sdk import OdealConfig, OdealClient
    from odeal_sdk.request_logger import OdealRequestLogger

    config = OdealConfig(
        secret_key='sk_xxx',
        interceptors=[OdealRequestLogger(level='info', mask_fields=['cvv', 'password'])]
    )
    client = OdealClient(config)
"""

import re
import logging
from typing import Callable, List, Optional

from .interceptor import OdealInterceptor, RequestContext, ResponseContext

DEFAULT_MASK_FIELDS = [
    'password', 'cvv', 'cvc', 'cardNumber', 'card_number', 'pan',
    'expiryDate', 'expiry_date', 'securityCode', 'security_code',
    'secretKey', 'secret_key', 'token', 'accessToken', 'access_token',
    'refreshToken', 'refresh_token', 'authorization',
    'tckn', 'tcKimlikNo', 'tcKimlik', 'identityNumber', 'nationalId',
    'iban', 'phone', 'phoneNumber', 'telephone', 'gsm',
    'email', 'eMail', 'mail', 'address', 'adres',
]


class OdealRequestLogger(OdealInterceptor):
    """
    Hazır Odeal Request Logger middleware'i.
    Tüm HTTP isteklerini ve yanıtlarını yapılandırılabilir şekilde loglar.
    """

    def __init__(
        self,
        level: str = 'info',
        min_duration_ms: float = 0,
        mask_fields: Optional[List[str]] = None,
        log_body: bool = True,
        log_response_body: bool = False,
        logger: Optional[Callable[[str, str], None]] = None,
    ):
        self.level = level
        self.min_duration_ms = min_duration_ms
        self.mask_fields = mask_fields or DEFAULT_MASK_FIELDS
        self.log_body = log_body
        self.log_response_body = log_response_body
        self._logger = logger or self._default_logger
        self._py_logger = logging.getLogger('odeal.sdk')

    def on_before_request(self, context: RequestContext) -> None:
        parts = [f"→ {context.method} {context.url}"]
        if self.log_body and context.body:
            parts.append(f"  Body: {self._mask_sensitive(context.body)}")
        self._log('\n'.join(parts), 'info')

    def on_after_response(self, context: ResponseContext) -> None:
        if context.duration_ms < self.min_duration_ms:
            return

        status = context.status_code
        level = 'error' if status >= 500 else 'warning' if status >= 400 else 'info'
        req = context.request
        parts = [
            f"← {status} {req.method if req else ''} {req.url if req else ''} ({context.duration_ms:.0f}ms)"
        ]
        if self.log_response_body and context.body:
            parts.append(f"  Body: {self._mask_sensitive(context.body[:500])}")
        self._log('\n'.join(parts), level)

    def _log(self, message: str, level: str) -> None:
        self._logger(f"[ODEAL {level.upper()}] {message}", level)

    def _default_logger(self, message: str, level: str) -> None:
        log_fn = getattr(self._py_logger, level, self._py_logger.info)
        log_fn(message)

    def _mask_sensitive(self, text: str) -> str:
        result = text
        for field in self.mask_fields:
            result = re.sub(
                rf'("{re.escape(field)}"\s*:\s*")[^"]+(")',
                r'\1***\2',
                result,
                flags=re.IGNORECASE
            )
        return result
