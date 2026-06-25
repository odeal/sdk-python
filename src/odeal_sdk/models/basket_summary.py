from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from ..utils import object_to_dict, deserialize

@dataclass
class BasketSummary:
    """
    Sepet listesindeki bir sepetin özeti.
    """
    
    _config_map = {
    }
    
    _validation_rules = {
    }
    id: Optional[int] = None
    """"""
    reference_code: Optional[str] = None
    """"""
    basket_alias: Optional[str] = None
    """"""
    basket_type: Optional[str] = None
    """"""
    status: Optional[str] = None
    """"""
    net_price: Optional[float] = None
    """"""
    gross_price: Optional[float] = None
    """"""
    vat_price: Optional[float] = None
    """"""
    sct_price: Optional[float] = None
    """"""
    acc_price: Optional[float] = None
    """"""
    customer_id: Optional[int] = None
    """"""
    device_id: Optional[int] = None
    """"""
    created_date: Optional[str] = None
    """"""

    def to_dict(self) -> Dict[str, Any]:
        return object_to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BasketSummary']:
        if not data:
            return None
        id = data.get("id")
        reference_code = data.get("referenceCode")
        basket_alias = data.get("basketAlias")
        basket_type = data.get("basketType")
        status = data.get("status")
        net_price = data.get("netPrice")
        gross_price = data.get("grossPrice")
        vat_price = data.get("vatPrice")
        sct_price = data.get("sctPrice")
        acc_price = data.get("accPrice")
        customer_id = data.get("customerId")
        device_id = data.get("deviceId")
        created_date = data.get("createdDate")

        return cls(
            id=id,
            reference_code=reference_code,
            basket_alias=basket_alias,
            basket_type=basket_type,
            status=status,
            net_price=net_price,
            gross_price=gross_price,
            vat_price=vat_price,
            sct_price=sct_price,
            acc_price=acc_price,
            customer_id=customer_id,
            device_id=device_id,
            created_date=created_date,
        )
