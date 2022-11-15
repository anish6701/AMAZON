from pydantic import BaseModel
from typing import Optional


class EmlBase(BaseModel):

    email :str
    otp:int
    status: Optional[int] = 0

    class Config():
        orm_mode=True

class Eml(BaseModel):
    otp:int

    class Config():
        orm_mode=True