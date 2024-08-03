from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from database import Base
from datetime import datetime
from general import tashkent


class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True)
	username = Column(String, unique=True)
	first_name = Column(String)
	last_name = Column(String)
	password = Column(String)
	is_active = Column(Boolean, default=True)
	role = Column(String)


class Assignment(Base):
	__tablename__ = "assignments"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(100), index=True)
	description = Column(String(255))
	priority = Column(Integer)
	complete = Column(Boolean, default=False)
	created_at = Column(DateTime, default=datetime.now(tz=tashkent))
	owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
