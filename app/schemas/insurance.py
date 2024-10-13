from sqlalchemy import BigInteger,  Column,Unicode, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin

class Insurance(Base, TimestampMixin):
    __tablename__ = "insurance"

    insurance_id = Column(BigInteger, primary_key=True, autoincrement=True)
    policy_number = Column(Unicode(255), nullable=False, unique=True)
    customer_id = Column(BigInteger, ForeignKey('customers.customer_id', ondelete='CASCADE'))
    insurance_url = Column(Unicode(255), nullable=True)
    customer = relationship("Customer", back_populates="insurance")
    __mapper_args__ = {"eager_defaults": True}
