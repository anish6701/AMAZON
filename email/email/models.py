from sqlalchemy import Column,Integer,String,SmallInteger,DateTime
from database import Base

class Email(Base):
    __tablename__='YOUR_TABLE_NAME'
    __table_args__ = {'extend_existing': True}

    user_id=Column(Integer,primary_key=True, index=True)
    email = Column(String(100))
    otp = Column(String(100))
    status = Column(SmallInteger)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
