"""
Odeal SDK Interceptor Modülü

HTTP istek/yanıt pipeline'ına araya girmek için kullanılan
interceptor abstract sınıfı ve context tipleri.

Örnek kullanım:
    class LoggingInterceptor(OdealInterceptor):
        def on_before_request(self, context: RequestContext) -> None:
            print(f"[REQUEST] {context.method} {context.url}")

        def on_after_response(self, context: ResponseContext) -> None:
            print(f"[RESPONSE] {context.status_code} ({context.duration_ms}ms)")

    config = OdealConfig(
        secret_key='sk_xxx',
        interceptors=[LoggingInterceptor()]
    )
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RequestContext:
    """İstek bağlamı — interceptor'a gönderilen istek bilgileri."""
    method: str = ''
    url: str = ''
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResponseContext:
    """Yanıt bağlamı — interceptor'a gönderilen yanıt bilgileri."""
    status_code: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    body: Optional[str] = None
    duration_ms: float = 0.0
    request: Optional[RequestContext] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class OdealInterceptor(ABC):
    """
    HTTP istek/yanıt pipeline'ına araya girmek için kullanılan abstract sınıf.
    İstek öncesi ve yanıt sonrası hook noktaları sunar.
    """

    def on_before_request(self, context: RequestContext) -> None:
        """HTTP isteği gönderilmeden önce çağrılır."""
        pass

    def on_after_response(self, context: ResponseContext) -> None:
        """HTTP yanıtı alındıktan sonra çağrılır."""
        pass
