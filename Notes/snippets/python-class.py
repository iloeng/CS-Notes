class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle:
    class_attribute = 10  # 类属性，被共享

    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    def area(self):
        return 3.14 * self._radius * self._radius


    _instance = None

    @staticmethod
    def getInstance(*args, **kwargs):
        if Circle._instance is None:
            Circle._instance = Circle(*args, **kwargs)
        return Circle._instance

    @classmethod
    def class_method(cls, new_value_for_attribute, radius_for_new_instance):
        cls.class_attribute = new_value_for_attribute
        print(f"Class attribute changed to: {cls.class_attribute}")
        return cls(radius_for_new_instance)

### singleton

class Singleton(type):
  _instances: Dict[type, "Singleton"] = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]

  def instance(cls: Any, *args: Any, **kwargs: Any) -> "Singleton":
    return cls(*args, **kwargs)

### 前向声明

from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class Schema(BaseModel):
    title: Optional[str] = None
    default: Optional[Any] = None
    type: Optional[str] = None
    anyOf: Optional[List['Schema']] = None  # 前向声明
    items: Optional['Schema'] = None  # 前向声明
    properties: Optional[Dict[str, 'Schema']] = None  # 前向声明