from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLITE
# DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(url=DATABASE_URL, connect_args={"check_same_thread": False})


# POSTGRESQL
DATABASE_URL = "postgresql://postgres:root_123@localhost:5432/todoapp"
engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
