"""
PaymentOptionType Enum Tanımı

Bu modül PaymentOptionType enum tipini içerir.
"""

from enum import Enum
from ..utils import StringEnum


class PaymentOptionType(StringEnum):
    """
    
    
    Bu enum StringEnum tipinden türetilmiştir ve API iletişiminde
    otomatik olarak doğru formata (string) serialize edilir.
    
    Values:
        CASH: 
        CREDITCARD: 
        GIFT: 
        OPENACCOUNT: 
        FOODCARD: 
    
    Example:
        >>> from odeal_sdk.enums import PaymentOptionType
        >>> value = PaymentOptionType.CASH
        >>> print(value.value)  # API'ye gönderilecek değer
    """
    CASH = "CASH"
    CREDITCARD = "CREDITCARD"
    GIFT = "GIFT"
    OPENACCOUNT = "OPEN_ACCOUNT"
    FOODCARD = "FOOD_CARD"

    def __str__(self) -> str:
        """String gösterimi."""
        return str(self.value)
    
    @classmethod
    def from_value(cls, value) -> 'PaymentOptionType':
        """
        Değerden enum oluşturur.
        
        Args:
            value: Enum değeri (API'den gelen).
            
        Returns:
            PaymentOptionType: Eşleşen enum değeri.
            
        Raises:
            ValueError: Geçersiz değer durumunda.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' geçerli bir PaymentOptionType değeri değil.")
