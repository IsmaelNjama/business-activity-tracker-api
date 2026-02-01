# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.sql import func
# from app.db.session import Base


# class Employee(Base):
#     __tablename__ = "employees"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True, nullable=False)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     email = Column(String, unique=True, index=True, nullable=False)
#     phone_number = Column(String, nullable=False)
#     gender = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(String, default="employee", nullable=False)
#     created_at = Column(DateTime(timezone=True),
#                         server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True),
#                         onupdate=func.now(), nullable=True)

#     def __repr__(self):
#         return (
#             f"<Employee "
#             f"username={self.username!r} "
#             f"id={self.id} "
#             f"email={self.email!r} "
#             f"first_name={self.first_name!r}"
#             f"last_name={self.last_name!r}>"
#         )
from __future__ import annotations


from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone_number: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default="employee")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())

    # Relationships
    activities: Mapped[list["Activity"]] = relationship(
        back_populates="employee")

    def __repr__(self):
        return (
            f"<Employee "
            f"username={self.username!r} "
            f"id={self.id} "
            f"email={self.email!r} "
            f"first_name={self.first_name!r} "
            f"last_name={self.last_name!r}>"
        )
