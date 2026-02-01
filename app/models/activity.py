from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Activity(Base):
    __tablename__ = "activities"

    # Core fields
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    # 'expense', 'sales', 'customer', 'production', 'storage'
    type: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # Expense fields
    # For expense and sales
    receipt_image: Mapped[Optional[str]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()  # For expense

    # Sales fields
    date: Mapped[Optional[str]] = mapped_column()
    time: Mapped[Optional[str]] = mapped_column()
    serving_employee: Mapped[Optional[str]] = mapped_column()
    buyer_name: Mapped[Optional[str]] = mapped_column()

    # Customer fields
    customer_name: Mapped[Optional[str]] = mapped_column()
    service_date: Mapped[Optional[str]] = mapped_column()
    service_type: Mapped[Optional[str]] = mapped_column()
    # For customer and production
    notes: Mapped[Optional[str]] = mapped_column()

    # Production fields
    raw_material_weight: Mapped[Optional[float]] = mapped_column()
    weight_unit: Mapped[Optional[str]] = mapped_column()
    machine_image_before: Mapped[Optional[str]] = mapped_column()
    machine_image_after: Mapped[Optional[str]] = mapped_column()

    # Storage fields
    location: Mapped[Optional[str]] = mapped_column()
    item_description: Mapped[Optional[str]] = mapped_column()
    quantity: Mapped[Optional[int]] = mapped_column()
    condition: Mapped[Optional[str]] = mapped_column()

    # Relationship to Employee
    employee: Mapped["Employee"] = relationship(back_populates="activities")

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "activity"
    }

    def __repr__(self):
        return f"<Activity id={self.id} type={self.type!r} user_id={self.user_id}>"
