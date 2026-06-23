import asyncio
from typing import Optional, List, Dict, Any, Union
from ..base_resource import BaseResource
from ..models import *
from ..utils import deserialize


class UnitResource(BaseResource):
    """
    Unit API Resource sınıfı.
    
    
    
    Bu sınıf BaseResource'dan türetilmiştir ve HTTP isteklerini yönetir.
    """

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
        """
        # Path oluşturma
        path = "/unit"

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
        from ..models.unit import Unit
        # [OTOMATİK] {"result":[...]} sarmalını listeye aç (BaseResource helper)
        response = self._unwrap_list(response)
        return [deserialize(item, Unit) for item in response]

    async def list_units_async(
        self,
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional[List['Unit']]:
        """
        Birimleri Listele (Async)
        
        sync list_units() metodunu asyncio.to_thread ile çağırır.

        Args:
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            List['Unit']: API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.list_units,
            secret_key,
            merchant_key,
            base_url,
        )