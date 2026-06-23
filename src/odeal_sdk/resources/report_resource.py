import asyncio
from typing import Optional, List, Dict, Any, Union
from ..base_resource import BaseResource
from ..models import *
from ..utils import deserialize


class ReportResource(BaseResource):
    """
    Report API Resource sınıfı.
    
    
    
    Bu sınıf BaseResource'dan türetilmiştir ve HTTP isteklerini yönetir.
    """

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
        """
        # Path oluşturma
        path = "/report/transactions"

        # Query parametreleri
        query_params: Dict[str, str] = {}
        if begin_date is not None:
            query_params["beginDate"] = str(begin_date)
        if end_date is not None:
            query_params["endDate"] = str(end_date)
        # externalDeviceKey: Config'den otomatik doldurulabilir
        _external_device_key = external_device_key
        if _external_device_key is None:
            _external_device_key = self.config.external_device_key
        if _external_device_key is not None:
            query_params["externalDeviceKey"] = str(_external_device_key)
        if basket_reference_code is not None:
            query_params["basketReferenceCode"] = str(basket_reference_code)

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
        from ..models.transaction_report import TransactionReport
        # [OTOMATİK] {"result":[...]} sarmalını listeye aç (BaseResource helper)
        response = self._unwrap_list(response)
        return [deserialize(item, TransactionReport) for item in response]

    async def get_transaction_report_async(
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
        İşlem Raporu (Async)
        
        sync get_transaction_report() metodunu asyncio.to_thread ile çağırır.

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
        """
        return await asyncio.to_thread(
            self.get_transaction_report,
            begin_date,
            end_date,
            secret_key,
            merchant_key,
            external_device_key,
            basket_reference_code,
            base_url,
        )