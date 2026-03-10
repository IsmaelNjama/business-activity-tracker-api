from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Literal, Union, Annotated
from datetime import datetime


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class ActivityBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        allow_population_by_field_name=True,
    )
    type: Literal["expense", "sales", "customer", "production", "storage"]
    user_id: str = Field(alias="userId")


class ExpenseActivityCreate(ActivityBase):
    type: Literal["expense"] = "expense"
    receipt_image: str
    description: Optional[str] = None


class SalesActivityCreate(ActivityBase):
    type: Literal["sales"] = "sales"
    receipt_image: str
    date: Union[int, str]
    time: Union[int, str]
    serving_employee: str
    buyer_name: str

    @field_validator("date", "time", mode="before")
    def _coerce_int(cls, v):
        if isinstance(v, str):
            digits = "".join(ch for ch in v if ch.isdigit())
            if digits:
                return int(digits)
        return v


class CustomerActivityCreate(ActivityBase):
    type: Literal["customer"] = "customer"
    customer_name: str = Field(alias="customerName")
    service_date: str = Field(alias="serviceDate")
    service_type: str = Field(alias="serviceType")
    notes: Optional[str] = None


class ProductionActivityCreate(ActivityBase):
    type: Literal["production"] = "production"
    raw_material_weight: Union[str, float, int]
    weight_unit: Union[int, str]
    machine_image_before: str
    machine_image_after: str
    notes: Optional[str] = None

    @field_validator("raw_material_weight", mode="before")
    def _weight_to_str(cls, v):
        if not isinstance(v, str):
            return str(v)
        return v

    @field_validator("weight_unit", mode="before")
    def _unit_to_int(cls, v):
        if isinstance(v, str):
            digits = "".join(ch for ch in v if ch.isdigit())
            if digits:
                return int(digits)
            # fallback: map common units to numbers if needed
            mapping = {"kg": 1, "lbs": 2}
            return mapping.get(v.lower(), v)
        return v


class StorageActivityCreate(ActivityBase):
    type: Literal["storage"] = "storage"
    location: str
    item_description: str
    quantity: int
    condition: str


# Union type for all activity creation types – discriminated on `type`
ActivityCreate = Annotated[
    Union[
        ExpenseActivityCreate,
        SalesActivityCreate,
        CustomerActivityCreate,
        ProductionActivityCreate,
        StorageActivityCreate,
    ],
    Field(discriminator="type"),
]


class ActivityOut(ActivityBase):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
        allow_population_by_field_name=True,
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
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        allow_population_by_field_name=True,
    )
    user_id: Optional[str] = Field(None, alias="userId")
    type: Optional[Literal["expense", "sales",
                           "customer", "production", "storage"]] = None
    start_date: Optional[str] = Field(None, alias="startDate")
    end_date: Optional[str] = Field(None, alias="endDate")


# updating activities
class ActivityUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True,
                              alias_generator=to_camel,
                              allow_population_by_field_name=True)
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
