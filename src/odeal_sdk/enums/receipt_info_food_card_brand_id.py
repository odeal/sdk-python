"""
ReceiptInfoFoodCardBrandId Enum Tanımı

Bu modül ReceiptInfoFoodCardBrandId enum tipini içerir.
"""

from enum import Enum
from ..utils import IntegerEnum


class ReceiptInfoFoodCardBrandId(IntegerEnum):
    """
    Koşullu. Eğer ödeme tipi 'FOOD_CARD' ise ZORUNLUDUR.
    /// - 100001: Multinet
    /// - 100002: Setcard
    /// - 100003: Edenred
    /// - 100004: Tokenflex
    /// - 100005: Pluxee
    /// - 100006: Metropol
    /// - 100007: Paye
    
    Bu enum IntegerEnum tipinden türetilmiştir ve API iletişiminde
    otomatik olarak doğru formata (sayı) serialize edilir.
    
    Values:
        MULTINET: 
        SETCARD: 
        EDENRED: 
        TOKENFLEX: 
        PLUXEE: 
        METROPOL: 
        PAYE: 
    
    Example:
        >>> from odeal_sdk.enums import ReceiptInfoFoodCardBrandId
        >>> value = ReceiptInfoFoodCardBrandId.MULTINET
        >>> print(value.value)  # API'ye gönderilecek değer
    """
    MULTINET = 100001
    SETCARD = 100002
    EDENRED = 100003
    TOKENFLEX = 100004
    PLUXEE = 100005
    METROPOL = 100006
    PAYE = 100007

    def __str__(self) -> str:
        """String gösterimi."""
        return str(self.value)
    
    @classmethod
    def from_value(cls, value) -> 'ReceiptInfoFoodCardBrandId':
        """
        Değerden enum oluşturur.
        
        Args:
            value: Enum değeri (API'den gelen).
            
        Returns:
            ReceiptInfoFoodCardBrandId: Eşleşen enum değeri.
            
        Raises:
            ValueError: Geçersiz değer durumunda.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' geçerli bir ReceiptInfoFoodCardBrandId değeri değil.")
