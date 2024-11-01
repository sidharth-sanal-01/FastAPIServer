from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database link for postgres
sqlite_url = "postgresql://postgres:12345678@localhost/FastAPI"

# engine for establishing session
engine = create_engine(sqlite_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# initialize db and close after evrything is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
