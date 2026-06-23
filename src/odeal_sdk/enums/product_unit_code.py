"""
ProductUnitCode Enum Tanımı

Bu modül ProductUnitCode enum tipini içerir.
"""

from enum import Enum
from ..utils import StringEnum


class ProductUnitCode(StringEnum):
    """
    Birim Kodları.
    /// - _3I: Kilogram-Adet (C# Uyumu için ön ekli)
    
    Bu enum StringEnum tipinden türetilmiştir ve API iletişiminde
    otomatik olarak doğru formata (string) serialize edilir.
    
    Values:
        C62: 
        CTM: 
        GRM: 
        GT: 
        MND: 
        KGM: 
        LTR: 
        MTK: 
        KWH: 
        MTQ: 
        MTR: 
        CMT: 
        B32: 
        CCT: 
        PR: 
        D30: 
        GFI: 
        KPO: 
        _3I: 
        KFO: 
        KHY: 
        KMA: 
        KNI: 
        KPH: 
        KSH: 
        KUR: 
        D32: 
        GWH: 
        MWH: 
        KWT: 
        LPA: 
        DMK: 
        NCL: 
        SM3: 
        R9: 
        SET: 
        T3: 
        AD: 
        PA: 
        PK: 
    
    Example:
        >>> from odeal_sdk.enums import ProductUnitCode
        >>> value = ProductUnitCode.C62
        >>> print(value.value)  # API'ye gönderilecek değer
    """
    C62 = "C62"
    CTM = "CTM"
    GRM = "GRM"
    GT = "GT"
    MND = "MND"
    KGM = "KGM"
    LTR = "LTR"
    MTK = "MTK"
    KWH = "KWH"
    MTQ = "MTQ"
    MTR = "MTR"
    CMT = "CMT"
    B32 = "B32"
    CCT = "CCT"
    PR = "PR"
    D30 = "D30"
    GFI = "GFI"
    KPO = "KPO"
    _3I = "3I"
    KFO = "KFO"
    KHY = "KHY"
    KMA = "KMA"
    KNI = "KNI"
    KPH = "KPH"
    KSH = "KSH"
    KUR = "KUR"
    D32 = "D32"
    GWH = "GWH"
    MWH = "MWH"
    KWT = "KWT"
    LPA = "LPA"
    DMK = "DMK"
    NCL = "NCL"
    SM3 = "SM3"
    R9 = "R9"
    SET = "SET"
    T3 = "T3"
    AD = "AD"
    PA = "PA"
    PK = "PK"

    def __str__(self) -> str:
        """String gösterimi."""
        return str(self.value)
    
    @classmethod
    def from_value(cls, value) -> 'ProductUnitCode':
        """
        Değerden enum oluşturur.
        
        Args:
            value: Enum değeri (API'den gelen).
            
        Returns:
            ProductUnitCode: Eşleşen enum değeri.
            
        Raises:
            ValueError: Geçersiz değer durumunda.
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' geçerli bir ProductUnitCode değeri değil.")
