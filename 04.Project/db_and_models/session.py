from sqlmodel import Session, SQLModel
from engine import engine


async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


async def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def drop_tables():
    SQLModel.metadata.drop_all(bind=engine)
