from sqlalchemy import Column,Integer,String,DateTime
from database import Base

class SMS(Base):
    __tablename__='YOUR_TABLE_NAME'
    __table_args__ = {'extend_existing': True}

    user_id=Column(Integer,primary_key=True, index=True)
    number = Column(String(100))
    otp = Column(String(100))
    status = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
