
from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
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

    
class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address