from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class Customer:
    """
    
    """
    
    _config_map = {
    }
    
    _validation_rules = {
        "reference_code": {"pattern": r"^.{0,50}$", "message": "ReferenceCode formatı geçersiz."
        },
        "name": {"pattern": r"^.{0,100}$", "message": "Name formatı geçersiz."
        },
        "surname": {"pattern": r"^.{0,100}$", "message": "Surname formatı geçersiz."
        },
        "identity_number": {"pattern": r"^[1-9]\d{10}$", "message": "TCKN 11 haneli olmalı."
        },
        "title": {"pattern": r"^.{0,255}$", "message": "Title formatı geçersiz."
        },
        "tax_number": {"pattern": r"^\d{10}$", "message": "VKN 10 haneli olmalı."
        },
        "tax_office": {"pattern": r"^.{0,100}$", "message": "TaxOffice formatı geçersiz."
        },
        "city": {"required": True,"pattern": r"^.{1,50}$", "message": "City formatı geçersiz."
        },
        "town": {"required": True,"pattern": r"^.{1,50}$", "message": "Town formatı geçersiz."
        },
        "gsm_number": {"pattern": r"^[1-9][0-9]{9}$", "message": "GSM No başında 0 olmadan 10 hane olmalıdır."
        },
        "email": {"pattern": r"^.{0,100}$", "message": "Email formatı geçersiz."
        },
        "address": {"pattern": r"^.{0,500}$", "message": "Address formatı geçersiz."
        },
    }
    reference_code: Optional[str] = None
    """Opsiyonel. Müşterinin kendi referans kodu."""
    type: Optional['CustomerType'] = None
    """Müşteri Tipi. Default: INDIVIDUAL."""
    name: Optional[str] = None
    """"""
    surname: Optional[str] = None
    """"""
    identity_number: Optional[str] = None
    """"""
    title: Optional[str] = None
    """"""
    tax_number: Optional[str] = None
    """"""
    tax_office: Optional[str] = None
    """"""
    city: Optional[str] = None
    """"""
    town: Optional[str] = None
    """"""
    gsm_number: Optional[str] = None
    """"""
    email: Optional[str] = None
    """"""
    address: Optional[str] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['Customer']:
        if not data:
            return None
        reference_code = data.get("referenceCode")
        # Nested Type: CustomerType
        from ..enums.customer_type import CustomerType
        type_raw = data.get("type")
        type = CustomerType(type_raw) if type_raw else None
        name = data.get("name")
        surname = data.get("surname")
        identity_number = data.get("identityNumber")
        title = data.get("title")
        tax_number = data.get("taxNumber")
        tax_office = data.get("taxOffice")
        city = data.get("city")
        town = data.get("town")
        gsm_number = data.get("gsmNumber")
        email = data.get("email")
        address = data.get("address")

        return cls(
            reference_code=reference_code,
            type=type,
            name=name,
            surname=surname,
            identity_number=identity_number,
            title=title,
            tax_number=tax_number,
            tax_office=tax_office,
            city=city,
            town=town,
            gsm_number=gsm_number,
            email=email,
            address=address,
        )
