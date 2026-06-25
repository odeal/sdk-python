"""
Odeal SDK Python Client

Bu modül Odeal API'sine erişim için ana istemci sınıfını içerir.
Facade tasarım deseni kullanılarak tüm kaynaklara tek noktadan erişim sağlanır.

Example:
    >>> from odeal_sdk import OdealClient, OdealConfig
    >>> 
    >>> config = OdealConfig(
    ...     secret_key="your-secret-key",
    ...     merchant_key="your-merchant-key",
    ... )
    >>> client = OdealClient(config)
    >>> 
    >>> # API çağrısı örneği
    >>> result = client.create_basket(request)
"""

from typing import Optional, List, Dict, Any, Union
from .odeal_config import OdealConfig

# --- MODEL IMPORTLARI ---
from .models import (
    BasketRequest,
    BasketRequestAdvance,
    BasketRequestCurrentAccount,
    BasketRequestFoodCard,
    ReceiptInfo,
    Customer,
    BasketPrice,
    Item,
    Product,
    ProductPrice,
    Exemption,
    PaymentOption,
    ConfigurationRequest,
    Unit,
    TransactionReport,
    BasketCreateResult,
    BasketSummary,
    BasketListResult,
    BasketResponse,
    BasketListResponse,
    CancelPaymentRequest,
    CancelPaymentResult,
    CancelPaymentResponse,
    ErrorResponse,
    ApiError,
    ValidationError,
    ConfigurationResponse,
)

# --- ENUM IMPORTLARI ---
from .enums import (
    BasketType,
    ReceiptInfoFoodCardBrandId,
    CustomerType,
    ProductUnitCode,
    PaymentOptionType,
)

# --- RESOURCE IMPORTLARI ---
from .resources.basket_resource import BasketResource
from .resources.payment_resource import PaymentResource
from .resources.configuration_resource import ConfigurationResource
from .resources.unit_resource import UnitResource
from .resources.report_resource import ReportResource


class OdealClient:
    """
    Odeal API Ana İstemcisi.
    
    Bu sınıf Facade tasarım deseni kullanarak tüm API kaynaklarına
    (resources) tek bir noktadan erişim sağlar.
    
    Attributes:
        config (OdealConfig): SDK yapılandırma ayarları.
        _basket (BasketResource): Basket resource instance'ı.
        _payment (PaymentResource): Payment resource instance'ı.
        _configuration (ConfigurationResource): Configuration resource instance'ı.
        _unit (UnitResource): Unit resource instance'ı.
        _report (ReportResource): Report resource instance'ı.
    
    Example:
        >>> config = OdealConfig(
        ...     base_url="https://api.odeal.com/v1",
        ...     secret_key="sk_...",
        ...     merchant_key="mk_...",
        ... )
        >>> client = OdealClient(config)
    """

    def __init__(self, config: OdealConfig) -> None:
        """
        OdealClient instance'ı oluşturur.
        
        Args:
            config: SDK yapılandırma ayarları.
        """
        self.config = config
        
        # Resource instance'larını oluştur
        self._basket = BasketResource(config)
        self._payment = PaymentResource(config)
        self._configuration = ConfigurationResource(config)
        self._unit = UnitResource(config)
        self._report = ReportResource(config)

    # ==========================================================================
    # RESOURCE ERİŞİMİ (gruplu)
    # ==========================================================================

    @property
    def basket(self) -> BasketResource:
        """Basket işlemlerine gruplu erişim (ör. ``client.basket.method(...)``).

        Aynı metotları doğrudan client üzerinden de çağırabilirsiniz (ör. ``client.method(...)``).
        """
        return self._basket

    @property
    def payment(self) -> PaymentResource:
        """Payment işlemlerine gruplu erişim (ör. ``client.payment.method(...)``).

        Aynı metotları doğrudan client üzerinden de çağırabilirsiniz (ör. ``client.method(...)``).
        """
        return self._payment

    @property
    def configuration(self) -> ConfigurationResource:
        """Configuration işlemlerine gruplu erişim (ör. ``client.configuration.method(...)``).

        Aynı metotları doğrudan client üzerinden de çağırabilirsiniz (ör. ``client.method(...)``).
        """
        return self._configuration

    @property
    def unit(self) -> UnitResource:
        """Unit işlemlerine gruplu erişim (ör. ``client.unit.method(...)``).

        Aynı metotları doğrudan client üzerinden de çağırabilirsiniz (ör. ``client.method(...)``).
        """
        return self._unit

    @property
    def report(self) -> ReportResource:
        """Report işlemlerine gruplu erişim (ör. ``client.report.method(...)``).

        Aynı metotları doğrudan client üzerinden de çağırabilirsiniz (ör. ``client.method(...)``).
        """
        return self._report

    # ==========================================================================
    # API METOTLARI
    # ==========================================================================

    # --------------------------------------------------------------------------
    # BASKET RESOURCE
    # --------------------------------------------------------------------------

    def create_simple_basket(
        self,
        request: 'BasketRequest',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Standart ürün satışı. Müşteri Bireysel veya Kurumsal olabilir. 'items' alanı zorunludur.
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.create_simple_basket(request=BasketRequest(...))
        """
        return self._basket.create_simple_basket(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def create_advance_basket(
        self,
        request: 'BasketRequestAdvance',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Avans tahsilatı. Müşteri Bireysel veya Kurumsal olabilir. 'items' gönderilmez. `basketType` ADVANCE olmalıdır.
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.create_advance_basket(request=BasketRequestAdvance(...))
        """
        return self._basket.create_advance_basket(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def create_current_account_basket(
        self,
        request: 'BasketRequestCurrentAccount',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Cari hesap tahsilatı. Müşteri Kurumsal olmalıdır. `basketType` CURRENT_ACCOUNT olmalıdır.
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.create_current_account_basket(request=BasketRequestCurrentAccount(...))
        """
        return self._basket.create_current_account_basket(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def create_food_card_basket(
        self,
        request: 'BasketRequestFoodCard',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Yemek kartı işlemleri. `receiptInfo` ve içindeki `foodCardBrandId` zorunludur.
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.create_food_card_basket(request=BasketRequestFoodCard(...))
        """
        return self._basket.create_food_card_basket(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def list_baskets(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        external_device_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketListResponse']:
        """
        Sepet Listele
        
        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            external_device_key:  (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketListResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.list_baskets()
        """
        return self._basket.list_baskets(
            secret_key=secret_key,
            merchant_key=merchant_key,
            external_device_key=external_device_key,
            base_url=base_url,
        )

    def delete_basket(
        self,
        reference_code: str,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Sepet Sil
        
        Args:
            reference_code: Silinecek sepetin referans kodu
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            None: Bu işlem yanıt döndürmez.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.delete_basket()
        """
        return self._basket.delete_basket(
            reference_code=reference_code,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def delete_all_baskets(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Tüm Sepetleri Sil
        
        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            None: Bu işlem yanıt döndürmez.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.delete_all_baskets()
        """
        return self._basket.delete_all_baskets(
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    # --------------------------------------------------------------------------
    # PAYMENT RESOURCE
    # --------------------------------------------------------------------------

    def cancel_payment(
        self,
        request: 'CancelPaymentRequest',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['CancelPaymentResponse']:
        """
        Ödeme İptali
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'CancelPaymentResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.cancel_payment(request=CancelPaymentRequest(...))
        """
        return self._payment.cancel_payment(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    # --------------------------------------------------------------------------
    # CONFIGURATION RESOURCE
    # --------------------------------------------------------------------------

    def save_configuration(
        self,
        request: 'ConfigurationRequest',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Konfigürasyon Kaydet
        
        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            None: Bu işlem yanıt döndürmez.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.save_configuration(request=ConfigurationRequest(...))
        """
        return self._configuration.save_configuration(
            request=request,
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    def get_configuration(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['ConfigurationResponse']:
        """
        Konfigürasyon Getir
        
        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'ConfigurationResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.get_configuration()
        """
        return self._configuration.get_configuration(
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    # --------------------------------------------------------------------------
    # UNIT RESOURCE
    # --------------------------------------------------------------------------

    def list_units(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional[List['Unit']]:
        """
        Birimleri Listele
        
        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            List['Unit']: API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.list_units()
        """
        return self._unit.list_units(
            secret_key=secret_key,
            merchant_key=merchant_key,
            base_url=base_url,
        )

    # --------------------------------------------------------------------------
    # REPORT RESOURCE
    # --------------------------------------------------------------------------

    def get_transaction_report(
        self,
        begin_date: str,
        end_date: str,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        external_device_key: Optional[str] = None,
        basket_reference_code: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional[List['TransactionReport']]:
        """
        İşlem Raporu
        
        Args:
            begin_date: 
            end_date: 
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            external_device_key:  (Opsiyonel)
            basket_reference_code:  (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            List['TransactionReport']: API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
            
        Example:
            >>> result = client.get_transaction_report()
        """
        return self._report.get_transaction_report(
            begin_date=begin_date,
            end_date=end_date,
            secret_key=secret_key,
            merchant_key=merchant_key,
            external_device_key=external_device_key,
            basket_reference_code=basket_reference_code,
            base_url=base_url,
        )

    def __repr__(self) -> str:
        """Okunabilir string gösterimi."""
        return f"OdealClient(base_url={self.config.base_url!r})"
