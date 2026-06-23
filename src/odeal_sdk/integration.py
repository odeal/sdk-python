"""
Odeal SDK Framework Integration Helpers

Django ve FastAPI gibi popüler Python framework'leri ile
kolay entegrasyon sağlayan yardımcı fonksiyonlar.

Django Kullanımı:
    # settings.py
    ODEAL_CONFIG = {
        'SECRET_KEY': 'sk_xxx',
        'MERCHANT_KEY': 'mk_xxx',
        'BASE_URL': 'https://api.odeal.com/v1',
    }

    # views.py
    from odeal_sdk.integration import get_odeal_client
    client = get_odeal_client()

FastAPI Kullanımı:
    from odeal_sdk.integration import odeal_client_dependency
    
    @app.post("/payment")
    async def create_payment(client = Depends(odeal_client_dependency)):
        return await client.basket.create(...)

Ortam Değişkenleri ile:
    from odeal_sdk.integration import create_client_from_env
    client = create_client_from_env()
"""

import os
from typing import Optional

from .odeal_config import OdealConfig


def create_client_from_env(
    secret_key_env: str = 'ODEAL_SECRET_KEY',
    merchant_key_env: str = 'ODEAL_MERCHANT_KEY',
    base_url_env: str = 'ODEAL_BASE_URL',
    **overrides
) -> 'OdealClient':
    """
    Ortam değişkenlerinden OdealClient oluşturur.
    
    Args:
        secret_key_env: Secret key ortam değişkeni adı.
        merchant_key_env: Merchant key ortam değişkeni adı.
        base_url_env: Base URL ortam değişkeni adı.
        **overrides: Config üzerine yazılacak değerler.
    
    Returns:
        Yapılandırılmış OdealClient instance'ı.
    
    Raises:
        EnvironmentError: Zorunlu ortam değişkenleri eksikse.
    """
    secret_key = os.environ.get(secret_key_env)
    merchant_key = os.environ.get(merchant_key_env)
    
    if not secret_key:
        raise EnvironmentError(f"{secret_key_env} environment variable must be set.")
    if not merchant_key:
        raise EnvironmentError(f"{merchant_key_env} environment variable must be set.")
    
    config = OdealConfig(
        secret_key=secret_key,
        merchant_key=merchant_key,
    )
    
    base_url = os.environ.get(base_url_env)
    if base_url:
        config.base_url = base_url
    
    debug = os.environ.get('ODEAL_DEBUG', '').lower()
    if debug == 'true':
        config.debug_mode = True
    
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    from .odeal_client import OdealClient
    return OdealClient(config)


def get_odeal_client() -> 'OdealClient':
    """
    Django settings'den OdealClient oluşturur.
    
    Django settings.py'de ODEAL_CONFIG dict'i tanımlanmış olmalıdır:
        ODEAL_CONFIG = {
            'SECRET_KEY': 'sk_xxx',
            'MERCHANT_KEY': 'mk_xxx',
        }
    
    Returns:
        Yapılandırılmış OdealClient instance'ı.
    
    Raises:
        ImportError: Django yüklü değilse.
        AttributeError: ODEAL_CONFIG settings'de tanımlı değilse.
    """
    try:
        from django.conf import settings
    except ImportError:
        raise ImportError("Django is required. Install it with: pip install django")
    
    odeal_settings = getattr(settings, 'ODEAL_CONFIG', None)
    if not odeal_settings:
        raise AttributeError("ODEAL_CONFIG must be defined in Django settings.")
    
    config = OdealConfig(
        secret_key=odeal_settings.get('SECRET_KEY', ''),
        merchant_key=odeal_settings.get('MERCHANT_KEY', ''),
        base_url=odeal_settings.get('BASE_URL', 'https://api.odeal.com/v1'),
        debug_mode=odeal_settings.get('DEBUG_MODE', False),
        timeout=odeal_settings.get('TIMEOUT', 30),
        max_retry_count=odeal_settings.get('MAX_RETRY_COUNT', 3),
    )
    
    from .odeal_client import OdealClient
    return OdealClient(config)


def odeal_client_dependency():
    """
    FastAPI Dependency Injection helper.
    
    Kullanım:
        from fastapi import Depends
        from odeal_sdk.integration import odeal_client_dependency
        
        @app.post("/payment")
        async def create_payment(client = Depends(odeal_client_dependency)):
            return client.basket.create(...)
    
    Returns:
        OdealClient instance'ı (ortam değişkenlerinden).
    """
    return create_client_from_env()
