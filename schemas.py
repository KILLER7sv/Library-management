
from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    # def __init__(self, city: str, country: str) -> None:
    #     self.city = city
    #     self.country = country
    city: str
    country: str

class Student(BaseModel):
    # def __init__(self, id: str, name: str, age: int, address: Address) -> None:
    #     self.name = name
    #     self.age = age
    #     self.address = Address
    #     self.id = id
    id:str = Field(None, allow_none=True)
    name: str
    age: int
    address: Address

class AddressUpdate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressUpdate] = None

    
