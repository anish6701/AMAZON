from fastapi import FastAPI
from routers import email



app=FastAPI(title='Email Service')
app.include_router(email.router)