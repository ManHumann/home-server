from fastapi import FastAPI
from app.routers import images

from app.database import test_connection

app = FastAPI()

app.include_router(images.router)

@app.on_event("startup")
def startup():
	print("Connecting to PostgreSQL...")
	test_connection()

@app.get("/")
def root():
	return {"status" : "running"}
