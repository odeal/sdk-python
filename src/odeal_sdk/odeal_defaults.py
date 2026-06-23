"""
Odeal SDK varsayılan değerleri ve HTTP durum kodu sabitleri.
"""


class OdealDefaults:
    """SDK genelinde kullanılan sabit değerler."""

    # --- Timeout & Retry ---
    TIMEOUT_SEC = 30
    MAX_RETRY_COUNT = 3
    BACKOFF_BASE_SEC = 0.5

    # --- Circuit Breaker ---
    CIRCUIT_BREAKER_THRESHOLD = 5
    CIRCUIT_BREAKER_RESET_MS = 60000

    # --- HTTP Status Codes ---
    HTTP_UNAUTHORIZED = 401
    HTTP_FORBIDDEN = 403
    HTTP_NOT_FOUND = 404
    HTTP_TOO_MANY_REQUESTS = 429

    @staticmethod
    def is_server_error(status_code: int) -> bool:
        return status_code >= 500

    @staticmethod
    def is_retryable(status_code: int) -> bool:
        return OdealDefaults.is_server_error(status_code) or status_code == OdealDefaults.HTTP_TOO_MANY_REQUESTS
