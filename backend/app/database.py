from sqlalchemy import create_engine , text , URL
from sqlalchemy.orm import sessionmaker , DeclarativeBase

from app import config

DATABASE_URL =DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
    database=config.DB_NAME,
)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)



def test_connection():
	with engine.connect() as connection:
		result = connection.execute(text("SELECT version();"))

	for row in result:
		print(row)

class Base(DeclarativeBase):
	pass
