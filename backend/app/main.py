from fastapi import FastAPI
from app.routers import images


from app.database import test_connection

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.96:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(images.router)

@app.on_event("startup")
def startup():
	print("Connecting to PostgreSQL...")
	test_connection()

@app.get("/")
def root():
	return {"status" : "running"}
