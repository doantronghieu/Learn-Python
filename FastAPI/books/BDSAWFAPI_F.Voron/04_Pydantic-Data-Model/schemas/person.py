from uu import Error
import add_packages
from enum import Enum
from datetime import date, datetime
from typing import Union
from pydantic import (
    BaseModel, ValidationError, Field, EmailStr, HttpUrl, model_validator, field_validator,
    root_validator,
)


class Gender(str, Enum):
    # Enum class for the gender field to specify valid values.
    # If an input value is not in this enumeration, Pydantic will raise an error.
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class Address(BaseModel):
    street_address: str
    postal_code: str
    city: str
    country: str


class Person(BaseModel):
    # The first positional argument sets the default value for the field.
    # For required fields, an ellipsis is used.
    # Keyword arguments set options for the field, including basic validation.

    # name arguments are required to be at least three characters long
    first_name: str = Field(..., min_length=3)
    last_name: str = Field(..., min_length=3)
    # age is optional and should be an integer between 0 and 120.
    age: Union[int, None] = Field(None, ge=0, le=120)
    gender: Gender
    # Date class as type for birthdate field. Pydantic able to automatically
    # parse dates and times as ISO format strings or timestamp integers and
    # instantiate proper date or datetime object.
    # If parsing fails, error will occur.
    birthdate: date
    interests: list[str]
    address: Address

    values: list[int]

    @field_validator("birthdate")
    # Validator is a static class method with the v argument being the value to
    # validate, cls is the class ifself. It’s decorated by the validator
    # decorator, which expects the name of the argument to validate to be its
    # first argument.
    def valid_birthdate(cls, v: date):
        # Checks a birth date by verifying person is not more than 120 years old.
        delta = date.today() - v
        age = delta.days / 365
        if age > 120:
            raise ValueError("You seem a bit too old!")
        return v

    @field_validator("values", mode="after")
    # Checks if there is a string. If so, split the comma-separated string and
    # return the list; otherwise, return the value.
    # Pydantic will run parsing logic to raise an error if v is invalid.
    def split_string_values(cls, v):
        if isinstance(v, str):
            return v.split(",")
        return v
      
    
    def name_dict(self):
      return self.model_dump(include={"first_name", "last_name"})


class UserProfile(BaseModel):
    nickname: str
    location: Union[str, None] = None
    subscribed_newsletter: bool = True

    email: EmailStr
    # URL parsed into object, giving access to different part (scheme, hostname).
    website: HttpUrl


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode="after")
    # The static class method is called along with the values argument, which is
    # a dictionary containing all the fields
    def passwords_match(cls, values: dict):
        password = values.get("password")
        password_confirmation = values.get("password_confirmation")
        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        return values

# *-----------------------------------------------------------------------------


# Creating a dummy person
dummy_person_data = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "gender": Gender.MALE,
    "birthdate": date(1992, 5, 15),
    "interests": ["Reading", "Traveling"],
    "address": {
        "street_address": "123 Main St",
        "postal_code": "12345",
        "city": "Example City",
        "country": "Example Country"
    },
    "values": [1, 2, 3]
}

dummy_person = Person(**dummy_person_data)
# transforms data into a dictionary. Sub-objects are recursively converted, 
# with the address key pointing to a dictionary with address properties.
dummy_person_dict = dummy_person.model_dump()

# The [in/ex]clude arguments expect a set with the keys of the fields to [in/ex]clude
dummy_person_include = dummy_person.model_dump(include={"first_name", "last_name"})
dummy_person_exclude = dummy_person.model_dump(exclude={"birthdate", "interests"})

# For nested structures, use a dictionary to specify sub-fields to include or exclude.
# Scalar fields have to be associated with the ellipsis, ....
dummy_person_nested_include = dummy_person.model_dump(
  include={
    "first_name": ...,
    "last_name": ...,
    "address": {"city", "country"},
  }
)