"""
Odeal SDK Circuit Breaker Modülü.

Art arda hata alındığında istekleri otomatik durdurur.
CLOSED → OPEN → HALF_OPEN → CLOSED
"""

import threading
import time
from enum import Enum
from typing import Optional


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class OdealCircuitOpenException(Exception):
    """Circuit breaker açık olduğunda fırlatılır."""
    def __init__(self, message: str = "Circuit breaker is open. Requests are temporarily blocked."):
        super().__init__(message)


class OdealCircuitBreaker:
    """
    Thread-safe Circuit Breaker implementasyonu.
    
    Args:
        failure_threshold: Ardışık hata eşiği (varsayılan: 5).
        reset_timeout_ms: OPEN durumunda bekleme süresi (milisaniye, varsayılan: 60000).
            Diğer dillerle ve ``config.circuit_breaker_reset_ms`` ile tutarlıdır.
    """

    def __init__(self, failure_threshold: int = 5, reset_timeout_ms: int = 60000):
        self._failure_threshold = failure_threshold
        self._reset_timeout_sec = reset_timeout_ms / 1000.0
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._half_open_probe_in_flight = False
        self._lock = threading.Lock()

    @property
    def current_state(self) -> CircuitState:
        """Mevcut durumu döner (yan etkisiz okuma)."""
        with self._lock:
            if (
                self._state == CircuitState.OPEN
                and self._last_failure_time is not None
                and (time.time() - self._last_failure_time) >= self._reset_timeout_sec
            ):
                return CircuitState.HALF_OPEN
            return self._state

    def allow_request(self) -> bool:
        """İsteğin geçip geçemeyeceğini kontrol eder.

        HALF_OPEN durumunda yalnızca TEK bir probe (test) isteğine izin verilir;
        probe sonuçlanana kadar diğer istekler reddedilir.
        """
        with self._lock:
            # OPEN -> HALF_OPEN: reset süresi dolduysa tek bir probe denemesine kapı aç.
            if (
                self._state == CircuitState.OPEN
                and self._last_failure_time is not None
                and (time.time() - self._last_failure_time) >= self._reset_timeout_sec
            ):
                self._state = CircuitState.HALF_OPEN
                self._half_open_probe_in_flight = False

            if self._state == CircuitState.CLOSED:
                return True
            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_probe_in_flight:
                    return False
                self._half_open_probe_in_flight = True  # probe izni bu isteğe verildi
                return True
            return False  # OPEN

    def record_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED
            self._half_open_probe_in_flight = False

    def record_failure(self) -> None:
        with self._lock:
            self._last_failure_time = time.time()

            if self._state == CircuitState.HALF_OPEN:
                # Probe başarısız -> doğrudan tekrar OPEN.
                self._state = CircuitState.OPEN
                self._half_open_probe_in_flight = False
                return

            self._failure_count += 1
            if self._failure_count >= self._failure_threshold:
                self._state = CircuitState.OPEN

    def reset(self) -> None:
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED
            self._last_failure_time = None
            self._half_open_probe_in_flight = False
