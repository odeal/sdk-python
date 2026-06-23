import asyncio
from typing import Optional, List, Dict, Any, Union
from ..base_resource import BaseResource
from ..models import *
from ..utils import deserialize


class BasketResource(BaseResource):
    """
    Basket API Resource sınıfı.
    
    
    
    Bu sınıf BaseResource'dan türetilmiştir ve HTTP isteklerini yönetir.
    """

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
        """
        # Path oluşturma
        path = "/basket"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="POST",
            path=path,
            body=request,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.basket_response import BasketResponse
        return deserialize(response, BasketResponse)

    async def create_simple_basket_async(
        self,
        request: 'BasketRequest',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Standart ürün satışı. Müşteri Bireysel veya Kurumsal olabilir. 'items' alanı zorunludur. (Async)
        
        sync create_simple_basket() metodunu asyncio.to_thread ile çağırır.

        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.create_simple_basket,
            request,
            secret_key,
            merchant_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/advance"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="POST",
            path=path,
            body=request,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.basket_response import BasketResponse
        return deserialize(response, BasketResponse)

    async def create_advance_basket_async(
        self,
        request: 'BasketRequestAdvance',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Avans tahsilatı. Müşteri Bireysel veya Kurumsal olabilir. 'items' gönderilmez. `basketType` ADVANCE olmalıdır. (Async)
        
        sync create_advance_basket() metodunu asyncio.to_thread ile çağırır.

        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.create_advance_basket,
            request,
            secret_key,
            merchant_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/current-account"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="POST",
            path=path,
            body=request,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.basket_response import BasketResponse
        return deserialize(response, BasketResponse)

    async def create_current_account_basket_async(
        self,
        request: 'BasketRequestCurrentAccount',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Cari hesap tahsilatı. Müşteri Kurumsal olmalıdır. `basketType` CURRENT_ACCOUNT olmalıdır. (Async)
        
        sync create_current_account_basket() metodunu asyncio.to_thread ile çağırır.

        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.create_current_account_basket,
            request,
            secret_key,
            merchant_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/foodCard"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="POST",
            path=path,
            body=request,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.basket_response import BasketResponse
        return deserialize(response, BasketResponse)

    async def create_food_card_basket_async(
        self,
        request: 'BasketRequestFoodCard',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketResponse']:
        """
        Yemek kartı işlemleri. `receiptInfo` ve içindeki `foodCardBrandId` zorunludur. (Async)
        
        sync create_food_card_basket() metodunu asyncio.to_thread ile çağırır.

        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.create_food_card_basket,
            request,
            secret_key,
            merchant_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/list"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)
        # externalDeviceKey: Config'den otomatik doldurulabilir
        _external_device_key = external_device_key
        if _external_device_key is None:
            _external_device_key = self.config.external_device_key
        if _external_device_key is not None:
            header_params["externalDeviceKey"] = str(_external_device_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="GET",
            path=path,
            body=None,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.basket_list_response import BasketListResponse
        return deserialize(response, BasketListResponse)

    async def list_baskets_async(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        external_device_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['BasketListResponse']:
        """
        Sepet Listele (Async)
        
        sync list_baskets() metodunu asyncio.to_thread ile çağırır.

        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            external_device_key:  (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'BasketListResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.list_baskets,
            secret_key,
            merchant_key,
            external_device_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/delete"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)
        if reference_code is not None:
            header_params["referenceCode"] = str(reference_code)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="DELETE",
            path=path,
            body=None,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        return None

    async def delete_basket_async(
        self,
        reference_code: str,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Sepet Sil (Async)
        
        sync delete_basket() metodunu asyncio.to_thread ile çağırır.

        Args:
            reference_code: Silinecek sepetin referans kodu
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            None: Bu işlem yanıt döndürmez.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.delete_basket,
            reference_code,
            secret_key,
            merchant_key,
            base_url,
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
        """
        # Path oluşturma
        path = "/basket/delete-all-baskets"

        # Query parametreleri
        query_params: Dict[str, str] = {}

        # Header parametreleri
        header_params: Dict[str, str] = {}
        # X-ODEAL-SECRET-KEY: Config'den otomatik doldurulabilir
        _secret_key = secret_key
        if _secret_key is None:
            _secret_key = self.config.secret_key
        if _secret_key is not None:
            header_params["X-ODEAL-SECRET-KEY"] = str(_secret_key)
        # X-ODEAL-MERCHANT-KEY: Config'den otomatik doldurulabilir
        _merchant_key = merchant_key
        if _merchant_key is None:
            _merchant_key = self.config.merchant_key
        if _merchant_key is not None:
            header_params["X-ODEAL-MERCHANT-KEY"] = str(_merchant_key)

        # Base URL belirleme
        target_base_url = base_url

        # API çağrısı
        response = self.send_request(
            method="DELETE",
            path=path,
            body=None,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        return None

    async def delete_all_baskets_async(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Tüm Sepetleri Sil (Async)
        
        sync delete_all_baskets() metodunu asyncio.to_thread ile çağırır.

        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            None: Bu işlem yanıt döndürmez.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.delete_all_baskets,
            secret_key,
            merchant_key,
            base_url,
        )