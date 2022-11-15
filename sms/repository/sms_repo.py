#Firstly importing required dependencies.
from operator import add
from turtle import update
from urllib import request
import boto3,math,random,datetime
from fastapi import HTTPException
from starlette import status
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, values, update 
from fastapi import HTTPException, status, Depends, Request
import models
import schemas

#Below using digits and generating 6 digits OTP.
digits = '0123456789' 
Otp = ''
for i in range(6):
    Otp += digits[math.floor(random.random() * 10)]
    otp = Otp
    msg = otp

#Below creating a function 'text', giving required parameters i.e "request" and "database(db)"".
def text(request:schemas.SmsBase, db: Session):
    client = boto3.client(
        "sns",
        aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
        aws_secret_access_key="YOUR_AWS_ACCESS_KEY",
    region_name="YOUR_REGION_NAME"
    )
#Send your sms.
    customer_no=request.number
    client.publish(
            PhoneNumber=customer_no,
            Message=f"Hi Greetings from 'ORGANIZATION_NAME'. \n The OTP is {otp}!"
    )
#Inserting data in the database table "SMS" assuming that table name is "SMS".
    test=models.SMS(number=request.number, 
                    otp = otp,
                    status = request.status,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                    )
    db.add(test)
    db.commit()
    db.refresh(test) 
    response = {"status": True,
                "message": "SMS Successfully Sent.",
                "Number":customer_no,
                "OTP": otp}  
    
    return response

#Creating a function verify which matches the entered OTP which is sent in the 'text' function.
def verify(request:schemas.Sms, db:Session):
    entered_otp = request.otp 

    #Below is the DB query written in SQLALCHEMY.
    result = db.query(models.SMS.user_id,models.SMS.otp).order_by(models.SMS.user_id.desc()).first()
    data = result

    saved_otp = data['otp']
    user_id1 = data['user_id']
    
    #Below giving if and else conditions to check the otp is valid and verifing the PhoneNumber.
    if entered_otp == int(saved_otp):
        result1 = db.query(models.SMS).filter(models.SMS.user_id == user_id1).first()
        result1.status = 1
        db.commit()
        db.refresh(result1)
        msg = {"status": "success",
               "OTP": f'{entered_otp}',
               "detail": f'PhoneNumber Verified'}
        return msg #If successfull then return success msg.
    else:
        msg = {"status": "failed",
               "detail": f'Entered OTP : {entered_otp} does not match'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=msg) #If unsuccessfull then raise exception.