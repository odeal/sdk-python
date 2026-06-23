import re
from enum import Enum
from typing import Any, Dict, List, Type, TypeVar, Union

T = TypeVar("T")

# --- STATİK ENUM TEMEL SINIFLARI ---
# C# Converter mantığı: Sınıfın kendisi tipini belli eder.

class StringEnum(str, Enum):
    """Metin tabanlı enumlar için temel sınıf (JSON: "DEGER")"""
    pass

class IntegerEnum(int, Enum):
    """Sayı tabanlı enumlar için temel sınıf (JSON: 100)"""
    pass

# -----------------------------------

def to_camel_case(snake_str: str) -> str:
    # ... (Mevcut kodlar aynı kalacak) ...
    if not snake_str: return snake_str
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def object_to_dict(obj: Any) -> Any:
    # ... (Mevcut kodlar aynı kalacak) ...
    if isinstance(obj, list):
        return [object_to_dict(i) for i in obj]
    
    if isinstance(obj, Enum):
        return obj.value
    
    if hasattr(obj, "__dict__"):
        result = {}
        for key, value in obj.__dict__.items():
            if key.startswith("_") or value is None: continue
            result[to_camel_case(key)] = object_to_dict(value)
        return result
    return obj

def deserialize(data: Any, cls: Type[T]) -> Union[T, Any]:
    # ... (Mevcut kodlar aynı kalacak) ...
    if data is None:
        return None
    if cls in (object, dict, str, int, float, bool, list):
        return data
    if hasattr(cls, "from_dict"):
        return cls.from_dict(data)
    if issubclass(cls, Enum):
        return cls(data)
    return data