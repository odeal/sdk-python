"""
Odeal Webhook İmza Doğrulama Modülü.

Example:
    >>> from odeal_sdk.webhook_verifier import OdealWebhookVerifier
    >>>
    >>> # Flask
    >>> @app.route('/webhook', methods=['POST'])
    ... def handle_webhook():
    ...     signature = request.headers.get('X-Odeal-Signature')
    ...     is_valid = OdealWebhookVerifier.verify_signature(
    ...         request.get_data(as_text=True),
    ...         signature,
    ...         'your-webhook-secret'
    ...     )
    ...     if not is_valid:
    ...         return 'Invalid signature', 401
"""

import hashlib
import hmac
import time
from typing import Optional, List, Union


class OdealWebhookVerifier:
    """Odeal webhook imzalarını doğrulama sınıfı."""

    SIGNATURE_HEADER = 'X-Odeal-Signature'
    TIMESTAMP_HEADER = 'X-Odeal-Timestamp'
    DEFAULT_TOLERANCE_SECONDS = 300  # 5 dakika

    @staticmethod
    def verify_signature(payload: str, signature: str, webhook_secret: str) -> bool:
        """
        Webhook imzasını doğrular (HMAC-SHA256).
        
        Args:
            payload: Ham webhook body.
            signature: X-Odeal-Signature header değeri.
            webhook_secret: Webhook secret key.
        
        Returns:
            İmza geçerliyse True.
        """
        if not payload or not signature or not webhook_secret:
            return False

        expected = OdealWebhookVerifier.compute_signature(payload, webhook_secret)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def verify_signature_multi(
        payload: str, signature: str, webhook_secrets: List[str]
    ) -> bool:
        """
        Birden fazla secret ile doğrulama (secret rotation desteği).
        Herhangi bir secret ile imza eşleşirse True döner.
        """
        if not payload or not signature or not webhook_secrets:
            return False
        for secret in webhook_secrets:
            if secret and OdealWebhookVerifier.verify_signature(payload, signature, secret):
                return True
        return False

    @staticmethod
    def verify_signature_with_timestamp(
        payload: str,
        signature: str,
        timestamp: str,
        webhook_secret: str,
        tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
    ) -> bool:
        """
        Timestamp kontrolü ile imza doğrulama (replay attack koruması).
        """
        try:
            epoch_seconds = int(timestamp)
        except (ValueError, TypeError):
            return False

        diff = abs(time.time() - epoch_seconds)
        if diff > tolerance_seconds:
            return False

        signed_payload = f"{timestamp}.{payload}"
        return OdealWebhookVerifier.verify_signature(signed_payload, signature, webhook_secret)

    @staticmethod
    def verify_signature_with_timestamp_multi(
        payload: str,
        signature: str,
        timestamp: str,
        webhook_secrets: List[str],
        tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS,
    ) -> bool:
        """Birden fazla secret + timestamp doğrulama (rotation + replay koruması)."""
        try:
            epoch_seconds = int(timestamp)
        except (ValueError, TypeError):
            return False

        diff = abs(time.time() - epoch_seconds)
        if diff > tolerance_seconds:
            return False

        signed_payload = f"{timestamp}.{payload}"
        return OdealWebhookVerifier.verify_signature_multi(signed_payload, signature, webhook_secrets)

    @staticmethod
    def compute_signature(payload: str, secret: str) -> str:
        """HMAC-SHA256 imza hesaplar."""
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
