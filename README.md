# Odeal SDK for Python

> Odeal Entegrasyon SDK (Otomatik Üretildi)

> **Version:** 2.17.8 | **License:** MIT | **Auto-Generated** by Odeal SDK Generator


## Installation

```bash
pip install odeal-sdk
```

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)

## Quick Start

```python
from odeal_sdk import OdealClient, OdealConfig

config = OdealConfig(
    secret_key="your-secret-key",
    merchant_key="your-merchant-key",
)
client = OdealClient(config)

# SDK iki kullanım biçimini de destekler — ikisi de eşdeğerdir, aynı metoda gider:
response = client.create_simple_basket(request)         # 1) Flat (doğrudan)
response = client.basket.create_simple_basket(request)  # 2) Grouped (resource üzerinden)
```

## Configuration

### Builder Pattern

```python
from odeal_sdk.odeal_config_builder import OdealConfigBuilder

config = (OdealConfigBuilder()
    .secret_key("sk_xxx")
    .merchant_key("mk_xxx")
    .base_url("https://api.odeal.com/v1")
    .debug_mode(True)
    .timeout(60)
    .max_retry_count(5)
    .build())

client = OdealClient(config)
```

### Environment Variables

```python
from odeal_sdk.integration import create_client_from_env

# Reads: ODEAL_SECRET_KEY, ODEAL_MERCHANT_KEY
client = create_client_from_env()
```

### Django Integration

```python
# settings.py
ODEAL_CONFIG = {
    'SECRET_KEY': 'sk_xxx',
    'MERCHANT_KEY': 'mk_xxx',
}

# views.py
from odeal_sdk.integration import get_odeal_client
client = get_odeal_client()
```

### FastAPI Integration

```python
from fastapi import Depends
from odeal_sdk.integration import odeal_client_dependency

@app.post("/payment")
async def create_payment(client=Depends(odeal_client_dependency)):
    return client.basket.create_simple_basket(request)
```

## Interceptors

```python
from odeal_sdk.interceptor import OdealInterceptor, RequestContext, ResponseContext

class LoggingInterceptor(OdealInterceptor):
    def on_before_request(self, ctx: RequestContext):
        print(f"→ {ctx.method} {ctx.url}")

    def on_after_response(self, ctx: ResponseContext):
        print(f"← {ctx.status_code} ({ctx.duration_ms:.0f}ms)")

config = OdealConfig(
    secret_key="sk_xxx",
    merchant_key="mk_xxx",
    interceptors=[LoggingInterceptor()],
)
```

## Error Handling

```python
from odeal_sdk.exceptions import (
    OdealApiException,
    OdealAuthenticationException,
    OdealRateLimitException,
    OdealNotFoundException,
)

try:
    client.basket.create_simple_basket(request)
except OdealRateLimitException as e:
    print(f"Rate limit! Retry: {e.retry_after_seconds}s")
except OdealAuthenticationException:
    print("Invalid API keys!")
except OdealNotFoundException:
    print("Resource not found")
except OdealApiException as e:
    print(f"API Error: {e.status_code} - {e.message}")
```

## Circuit Breaker

```python
config = OdealConfig(
    secret_key="sk_xxx",
    merchant_key="mk_xxx",
    circuit_breaker_enabled=True,
    circuit_breaker_threshold=5,      # 5 consecutive failures → circuit opens
    circuit_breaker_reset_sec=60.0,   # 60s cooldown before half-open test
)

from odeal_sdk.circuit_breaker import OdealCircuitOpenException

try:
    client.basket.create_simple_basket(request)
except OdealCircuitOpenException:
    print("Circuit open — requests temporarily blocked.")
```

## Request Logger

Built-in `OdealRequestLogger` middleware for production HTTP traffic logging:

```python
from odeal_sdk import OdealConfig, OdealClient
from odeal_sdk.request_logger import OdealRequestLogger

config = OdealConfig(
    secret_key='sk_xxx',
    interceptors=[
        OdealRequestLogger(
            level='info',
            mask_fields=['password', 'cvv', 'cardNumber', 'tckn', 'iban', 'email', 'phone', 'address'],
            log_body=True,
            log_response_body=False,
            min_duration_ms=0,
        )
    ]
)
client = OdealClient(config)

# Output:
# [ODEAL INFO] → POST https://api.odeal.com/basket/simple
#   Body: {"merchantKey":"mk_xxx","password":"***"}
# [ODEAL INFO] ← 200 POST https://api.odeal.com/basket/simple (142ms)
```

Integration with Python `logging` module:

```python
import logging
logging.basicConfig(level=logging.INFO)

# OdealRequestLogger automatically uses the 'odeal.sdk' logger
```

## Timeout & Retry

```python
config = OdealConfig(
    timeout=60,           # Default: 30s
    max_retry_count=5,    # Default: 3
)

# Automatic retry on 5xx and 429 with exponential backoff
# Retry-After header is respected
```

## Async Usage

```python
import asyncio

async def main():
    # Single async request
    result = await client.basket.create_simple_basket_async(request)

    # Multiple concurrent requests
    results = await asyncio.gather(
        client.basket.create_simple_basket_async(req1),
        client.basket.create_simple_basket_async(req2),
    )

asyncio.run(main())
```

## Webhook Verification

Gelen Odeal webhook'larının gerçekten Odeal'den geldiğini HMAC-SHA256 imzasıyla doğrulayın.
İmza `X-Odeal-Signature` header'ında, **ham gövde** üzerinden hesaplanarak gelir.

```python
from flask import Flask, request, abort
from odeal_sdk import OdealWebhookVerifier

app = Flask(__name__)

@app.post("/webhooks/odeal")
def handle_webhook():
    payload = request.get_data(as_text=True)  # ham gövde
    signature = request.headers.get(OdealWebhookVerifier.SIGNATURE_HEADER, "")

    if not OdealWebhookVerifier.verify_signature(payload, signature, "your-webhook-secret"):
        abort(401, "Invalid webhook signature")

    # İmza geçerli — webhook olayını işle
    return "", 200
```

Replay koruması için timestamp doğrulamalı sürüm (önerilir):

```python
valid = OdealWebhookVerifier.verify_signature_with_timestamp(
    payload, signature, timestamp, "your-webhook-secret")  # varsayılan 5 dk tolerans
```

## Features

- ✅ Python 3.8+ compatible
- ✅ Zero external dependencies (stdlib only)
- ✅ Builder pattern for clean configuration
- ✅ Django & FastAPI integration helpers
- ✅ Interceptor pipeline (request/response hooks)
- ✅ Rich error hierarchy (Auth, Forbidden, NotFound, RateLimit, Validation)
- ✅ Automatic retry with exponential backoff & Retry-After header
- ✅ Configurable timeout
- ✅ Idempotency key injection for POST/PUT/PATCH
- ✅ Client-side input validation
- ✅ Sensitive data masking in debug logs
- ✅ Response unwrapping (`{"result": [...]}` → auto-extract)
- ✅ Circuit breaker pattern
- ✅ Request Logger middleware
- ✅ Async support (`asyncio.to_thread`)
- ✅ Webhook signature verification
- ✅ Health check utility

## API Reference
### BasketResource

| Method | Description |
|:-------|:------------|
| `create_simple_basket()` | Standart ürün satışı. Müşteri Bireysel veya Kurumsal olabilir. 'items' alanı zorunludur. |
| `create_advance_basket()` | Avans tahsilatı. Müşteri Bireysel veya Kurumsal olabilir. 'items' gönderilmez. `basketType` ADVANCE olmalıdır. |
| `create_current_account_basket()` | Cari hesap tahsilatı. Müşteri Kurumsal olmalıdır. `basketType` CURRENT_ACCOUNT olmalıdır. |
| `create_food_card_basket()` | Yemek kartı işlemleri. `receiptInfo` ve içindeki `foodCardBrandId` zorunludur. |
| `list_baskets()` | Sepet Listele |
| `delete_basket()` | Sepet Sil |
| `delete_all_baskets()` | Tüm Sepetleri Sil |
### PaymentResource

| Method | Description |
|:-------|:------------|
| `cancel_payment()` | Ödeme İptali |
### ConfigurationResource

| Method | Description |
|:-------|:------------|
| `save_configuration()` | Konfigürasyon Kaydet |
| `get_configuration()` | Konfigürasyon Getir |
### UnitResource

| Method | Description |
|:-------|:------------|
| `list_units()` | Birimleri Listele |
### ReportResource

| Method | Description |
|:-------|:------------|
| `get_transaction_report()` | İşlem Raporu |

## 🔐 Güvenlik & Doğrulama

Bu paket **Sigstore (cosign)** ile imzalanır ve doğrulanabilir kanıtlarla (attestation) yayınlanır:

- **İmza** — keyless cosign imzası; kimlik, yayınlayan CI workflow'una OIDC ile bağlanır
- **SBOM** — CycloneDX yazılım malzeme listesi (imzalı attestation)
- **Zafiyet taraması** — grype taraması (imzalı attestation)
- **Provenance** — SLSA build-provenance attestation'ı

### Doğrulama

```bash
# Paket imzası
cosign verify-blob \
  --bundle sign.bundle.json \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp "<yayın-workflow-url>" \
  <paket-dosyası>

# SBOM attestation
cosign verify-blob-attestation \
  --bundle sbom.bundle.json --type cyclonedx \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp "<yayın-workflow-url>" \
  <paket-dosyası>
```

Güvenlik açığı bildirimi ve tam talimatlar için: [`SECURITY.md`](./SECURITY.md)


## License

MIT
