from sqlalchemy import Integer,  Column,Unicode, ForeignKey,DateTime
from sqlalchemy.orm import relationship

from core.database.session import Base

class Insurance(Base):
    __tablename__ = "customer_insurance"
    customer_policy_id = Column(Integer, primary_key=True, autoincrement=True)
    insurance_id = Column(Integer, nullable=False)
    policy_number = Column(Unicode(255), nullable=False, unique=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='CASCADE'))
    customer_policy_url = Column(Unicode(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    customer = relationship("Customer", back_populates="insurance")
    __mapper_args__ = {"eager_defaults": True}
