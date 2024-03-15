from enum import Enum

from pydantic import BaseModel


class UserType(str, Enum):
    # Define string enumeration by inheriting from str type and Enum class.
    # List allowed values as class properties: property name and string value.
    STANDARD = "standard"
    ADMIN = "admin"


class UsersFormat(str, Enum):
    SHORT = "short"
    FULL = "full"


class User(BaseModel):
    name: str
    age: int


class Company(BaseModel):
    # Pydantic model with a single string name property.
    name: str
