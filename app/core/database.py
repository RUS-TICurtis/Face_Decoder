from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{settings.STORAGE_DIR}/{sqlite_file_name}"

# echo=False for production, True for debugging SQL
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
