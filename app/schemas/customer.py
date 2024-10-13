from sqlalchemy import BigInteger, Column, Unicode
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    customer_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), nullable=False, unique=True)

    insurance = relationship(
        "Insurance", back_populates="customer", lazy="raise", passive_deletes=True
    )

    __mapper_args__ = {"eager_defaults": True}
