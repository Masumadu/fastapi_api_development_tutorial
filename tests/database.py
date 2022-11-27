from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://admin:admin@localhost:5432/test_fastapi"

# for establishing a connection to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# for communicating or talking to postgres
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
