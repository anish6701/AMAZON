from pydantic import BaseModel
from typing import Optional


class SmsBase(BaseModel):
    number :str
    otp:int
    status: Optional[int] = 0
    class Config():
        orm_mode=True

class Sms(BaseModel):
    otp:int
    class Config():
        orm_mode=True

class Sms_one(BaseModel):
    number:str="+91"
    status: Optional[int] = 0
    class Config():
        orm_mode=True
