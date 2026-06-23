"""
API bağlantı durumunu kontrol eder.

Kullanım::

    health_check = OdealHealthCheck(config)
    result = health_check.ping()
    print(f"API: {'✓' if result.is_healthy else '✗'} ({result.latency_ms}ms)")
"""
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Optional


@dataclass
class HealthCheckResult:
    """Health check sonucu."""
    is_healthy: bool
    status_code: int
    latency_ms: int
    base_url: str
    error_message: Optional[str] = None

    def __str__(self) -> str:
        if self.is_healthy:
            return f"✓ Healthy ({self.latency_ms}ms) {self.base_url}"
        return f"✗ Unhealthy ({self.latency_ms}ms) {self.base_url} — {self.error_message or f'HTTP {self.status_code}'}"


class OdealHealthCheck:
    """API bağlantı kontrol sınıfı."""

    def __init__(self, config):
        self._config = config

    def ping(self) -> HealthCheckResult:
        """API'ye basit bir GET isteği göndererek bağlantıyı test eder."""
        start = time.monotonic()
        try:
            req = urllib.request.Request(
                f"{self._config.base_url}/health",
                headers={"X-ODEAL-SECRET-KEY": self._config.secret_key or ""},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                latency_ms = int((time.monotonic() - start) * 1000)
                return HealthCheckResult(
                    is_healthy=200 <= response.status < 400,
                    status_code=response.status,
                    latency_ms=latency_ms,
                    base_url=self._config.base_url,
                )
        except urllib.error.HTTPError as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            return HealthCheckResult(
                is_healthy=False,
                status_code=e.code,
                latency_ms=latency_ms,
                base_url=self._config.base_url,
                error_message=str(e),
            )
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            return HealthCheckResult(
                is_healthy=False,
                status_code=0,
                latency_ms=latency_ms,
                base_url=self._config.base_url,
                error_message=str(e),
            )

