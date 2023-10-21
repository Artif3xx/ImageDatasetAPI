"""
this is the main database file for the crud repository.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# link the sqlite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///././data/Database.db"

# create a sql alchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# define the local session with the given engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define the Base declaration
Base = declarative_base()


# Dependency
def get_db():
    """
    get the session database for queries

    :return: the session database object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
