from fastapi import FastAPI


from app.database import test_connection

app = FastAPI()


@app.on_event("startup")
def startup():
	print("Connecting to PostgreSQL...")
	test_connection()

@app.get("/")
def root():
	return {"status" : "running"}
