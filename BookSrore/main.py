
from fastapi import FastAPI
from routes import router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Book Management API 📚🚀"}

app.include_router(router, prefix="/api")
