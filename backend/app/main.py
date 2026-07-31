from fastapi import FastAPI
from app.routers import images


from app.database import test_connection

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.1.96",
        "http://192.168.1.96:80",
        "http://192.168.1.96:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(images.router)


@app.on_event("startup")
def startup():
    print("Connecting to PostgreSQL...")

    for attempt in range(10):
        try:
            test_connection()
            print("Connected!")
            return
        except OperationalError:
            print(f"Attempt {attempt + 1}/10 failed...")
            time.sleep(2)

    raise Exception("Could not connect to PostgreSQL.")


@app.get("/")
def root():
	return {"status" : "running"}
