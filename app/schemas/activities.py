from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class ActivityBase(BaseModel):
    type: Literal["expense", "sales", "customer", "production", "storage"]


class ExpenseActivityCreate(ActivityBase):
    type: Literal["expense"]
    receipt_image: str
    description: Optional[str] = None


class SalesActivityCreate(ActivityBase):
    type: Literal["sales"]
    receipt_image: str
    date: int
    time: int
    serving_employee: str
    buyer_name: str


class CustomerActivityCreate(ActivityBase):
    type: Literal["customer"]
    customer_name: str
    service_date: str
    service_type: str
    notes: Optional[str] = None


class ProductionActivityCreate(ActivityBase):
    type: Literal["production"]
    raw_material_weight: str
    weight_unit: int
    machine_image_before: str
    machine_image_after: str
    notes: Optional[str] = None


class StorageActivityCreate(ActivityBase):
    type: Literal["storage"]
    location: str
    item_description: str
    quantity: int
    condition: str
