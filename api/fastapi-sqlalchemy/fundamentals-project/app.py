from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EchoInput(BaseModel):
    message: str

@app.get('/')
def welcome():
    return {"message": "Welcome to my API!"}

@app.get('/hello')
def hello():
    return {"message": "Hello, World!"}

@app.get('/status')
def status():
    return {"status": "ok", "version": "1.0"}

@app.post('/echo')
def echo(body: EchoInput):
    return {"you_sent": body.message}