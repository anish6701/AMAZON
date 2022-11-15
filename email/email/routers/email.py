from fastapi import APIRouter, status
import schemas
from repository import email


router = APIRouter(
    prefix="/email",
    tags=['Email_Verification']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def send():
    return email.mail()

@router.put('/',status_code=status.HTTP_202_ACCEPTED)
def check(request:schemas.Eml):
    return email.verify(request)