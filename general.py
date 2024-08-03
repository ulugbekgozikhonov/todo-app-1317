from fastapi import Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from database import engine, SessionLocal
from pytz import timezone

tashkent = timezone("Asia/Tashkent")


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_dependency = Annotated[Session, Depends(get_db)]
