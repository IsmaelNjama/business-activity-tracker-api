from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, Union
from datetime import datetime


class ActivityBase(BaseModel):
    type: Literal["expense", "sales", "customer", "production", "storage"]
    user_id: str = Field(alias="userId")


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


# Union type for all activity creation types
ActivityCreate = Union[
    ExpenseActivityCreate,
    SalesActivityCreate,
    CustomerActivityCreate,
    ProductionActivityCreate,
    StorageActivityCreate
]


class ActivityOut(ActivityBase):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    id: str
    user_id: str = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    receipt_image: Optional[str] = None
    description: Optional[str] = None
    date: Optional[int] = None
    time: Optional[int] = None
    serving_employee: Optional[str] = None
    buyer_name: Optional[str] = None
    customer_name: Optional[str] = None
    service_date: Optional[str] = None
    service_type: Optional[str] = None
    notes: Optional[str] = None
    raw_material_weight: Optional[str] = None
    weight_unit: Optional[int] = None
    machine_image_before: Optional[str] = None
    machine_image_after: Optional[str] = None
    location: Optional[str] = None
    item_description: Optional[str] = None
    quantity: Optional[int] = None
    condition: Optional[str] = None


# filtering activities
class ActivityFilters(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_id: Optional[str] = Field(None, alias="userId")
    type: Optional[Literal["expense", "sales",
                           "customer", "production", "storage"]] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")


# updating activities
class ActivityUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Optional[Literal["expense", "sales",
                           "customer", "production", "storage"]] = None

    receipt_image: Optional[str] = None
    description: Optional[str] = None
    date: Optional[int] = None
    time: Optional[int] = None
    serving_employee: Optional[str] = None
    buyer_name: Optional[str] = None
    customer_name: Optional[str] = None
    service_date: Optional[str] = None
    service_type: Optional[str] = None
    notes: Optional[str] = None
    raw_material_weight: Optional[str] = None
    weight_unit: Optional[int] = None
    machine_image_before: Optional[str] = None
    machine_image_after: Optional[str] = None
    location: Optional[str] = None
    item_description: Optional[str] = None
    quantity: Optional[int] = None
    condition: Optional[str] = None
