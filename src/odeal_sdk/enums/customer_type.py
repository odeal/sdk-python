"""
CustomerType Enum Tanımı

Bu modül CustomerType enum tipini içerir.
"""

from enum import Enum
from ..utils import StringEnum


class CustomerType(StringEnum):
    """
    Müşteri Tipi. Default: INDIVIDUAL.
    
    Bu enum StringEnum tipinden türetilmiştir ve API iletişiminde
    otomatik olarak doğru formata (string) serialize edilir.
    
    Values:
        INDIVIDUAL: 
        CORPORATE: 
    
    Example:
        >>> from odeal_sdk.enums import CustomerType
        >>> value = CustomerType.INDIVIDUAL
        >>> print(value.value)  # API'ye gönderilecek değer
    """
    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"

    def __str__(self) -> str:
        """String gösterimi."""
        return str(self.value)
    
    @classmethod
    def from_value(cls, value) -> 'CustomerType':
        """
        Değerden enum oluşturur.
        
        Args:
            value: Enum değeri (API'den gelen).
            
        Returns:
            CustomerType: Eşleşen enum değeri.
            
        Raises:
            ValueError: Geçersiz değer durumunda.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' geçerli bir CustomerType değeri değil.")
