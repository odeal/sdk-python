"""
Odeal API ortam tanımları.

Kullanım::

    from odeal_sdk.odeal_environment import OdealEnvironment

    config = OdealConfigBuilder() \\
        .secret_key("sk_xxx") \\
        .environment(OdealEnvironment.PRODUCTION) \\
        .build()
"""
from enum import Enum


class OdealEnvironment(Enum):
    """Odeal API ortam enum'u."""

    STAGING = "staging"
    """Test/geliştirme ortamı."""

    PRODUCTION = "production"
    """Canlı (production) ortamı."""

    def get_base_url(self) -> str:
        """Ortam için API base URL'ini döner."""
        if self == OdealEnvironment.PRODUCTION:
            return "https://api.odeal.com/v1"
        return "https://stage.odealapp.com/api/v1"
