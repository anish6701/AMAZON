from fastapi import APIRouter, Depends, status, HTTPException, Response
import database,  schemas
from sqlalchemy.orm import Session
from typing import List
from repository import sms_repo


router = APIRouter(
    prefix="/sms",
    tags=['SMS_Verification']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def send(request:schemas.Sms_one, db:Session=Depends(database.get_db)):
    return sms_repo.text(request, db)

@router.put('/',status_code=status.HTTP_202_ACCEPTED)
def check(request:schemas.Sms, db:Session=Depends(database.get_db)):
    return sms_repo.verify(request, db)