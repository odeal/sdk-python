"""
BasketType Enum Tanımı

Bu modül BasketType enum tipini içerir.
"""

from enum import Enum
from ..utils import StringEnum


class BasketType(StringEnum):
    """
    Global Basket Type Enum.
    
    Bu enum StringEnum tipinden türetilmiştir ve API iletişiminde
    otomatik olarak doğru formata (string) serialize edilir.
    
    Values:
        SIMPLE: 
        ADVANCE: 
        CURRENTACCOUNT: 
    
    Example:
        >>> from odeal_sdk.enums import BasketType
        >>> value = BasketType.SIMPLE
        >>> print(value.value)  # API'ye gönderilecek değer
    """
    SIMPLE = "SIMPLE"
    ADVANCE = "ADVANCE"
    CURRENTACCOUNT = "CURRENT_ACCOUNT"

    def __str__(self) -> str:
        """String gösterimi."""
        return str(self.value)
    
    @classmethod
    def from_value(cls, value) -> 'BasketType':
        """
        Değerden enum oluşturur.
        
        Args:
            value: Enum değeri (API'den gelen).
            
        Returns:
            BasketType: Eşleşen enum değeri.
            
        Raises:
            ValueError: Geçersiz değer durumunda.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' geçerli bir BasketType değeri değil.")
