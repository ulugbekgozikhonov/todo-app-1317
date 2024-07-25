from sqlalchemy import Column, Integer, String, Boolean, DateTime

from database import Base
from pytz import timezone
from datetime import datetime

tashkent = timezone("Asia/Tashkent")
print(tashkent)


class AssignmentModel(Base):
	__tablename__ = "assignments"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(100), index=True)
	description = Column(String(255))
	priority = Column(Integer)
	complete = Column(Boolean, default=False)
	created_at = Column(DateTime, default=datetime.now(tz=tashkent), onupdate=False)
