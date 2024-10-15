from sqlalchemy import Integer, Column, Unicode
from sqlalchemy.orm import relationship

from core.database.session import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)

    insurance = relationship(
        "Insurance", back_populates="customer", lazy="raise", passive_deletes=True
    )

    __mapper_args__ = {"eager_defaults": True}
