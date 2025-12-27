from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="employee", nullable=False)

    def __repr__(self):
        return (
            f"<Employee "
            f"user_name={self.user_name!r} "
            f"id={self.id} "
            f"email={self.email!r} "
            f"first_name={self.first_name!r}"
            f"last_name={self.last_name!r}>"
        )
