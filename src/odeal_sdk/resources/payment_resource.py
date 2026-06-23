import asyncio
from typing import Optional, List, Dict, Any, Union
from ..base_resource import BaseResource
from ..models import *
from ..utils import deserialize


class PaymentResource(BaseResource):
    """
    Payment API Resource sınıfı.
    
    
    
    Bu sınıf BaseResource'dan türetilmiştir ve HTTP isteklerini yönetir.
    """

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
        """
        # Path oluşturma
        path = "/payment/cancel"

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
            method="PUT",
            path=path,
            body=request,
            query_params=query_params if query_params else None,
            headers=header_params if header_params else None,
            base_url=target_base_url,
        )
        # Yanıt dönüştürme
        if response is None:
            return None
        from ..models.cancel_payment_response import CancelPaymentResponse
        return deserialize(response, CancelPaymentResponse)

    async def cancel_payment_async(
        self,
        request: 'CancelPaymentRequest',
        secret_key: Optional[str] = None,
        merchant_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> Optional['CancelPaymentResponse']:
        """
        Ödeme İptali (Async)
        
        sync cancel_payment() metodunu asyncio.to_thread ile çağırır.

        Args:
            request: request parametresi.
            secret_key: Size özel olarak verilmiş gizli anahtar. (Opsiyonel)
            merchant_key: Size özel olarak verilmiş iş yeri anahtarı. (Opsiyonel)
            base_url: Alternatif API base URL'i. (Opsiyonel)
            
        Returns:
            'CancelPaymentResponse': API yanıtı.
            
        Raises:
            OdealApiException: API hatası durumunda.
        """
        return await asyncio.to_thread(
            self.cancel_payment,
            request,
            secret_key,
            merchant_key,
            base_url,
        )