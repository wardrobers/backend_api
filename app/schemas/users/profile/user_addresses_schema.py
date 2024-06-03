from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel


class AddressType(str, Enum):
    Shipping = "Shipping"
    Billing = "Billing"
    Both = "Both"


class UserAddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    country: str
    postal_code: str


class UserAddressCreate(UserAddressBase):
    address_type: AddressType


class UserAddressUpdate(UserAddressBase):
    address_type: Optional[AddressType] = None


class UserAddressRead(UserAddressBase):
    id: UUID4
    user_id: UUID4
    address_type: AddressType
