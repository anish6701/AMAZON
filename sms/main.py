from fastapi import FastAPI
from routers import sms_rout

app=FastAPI(title='SMS Service')

app.include_router(sms_rout.router)