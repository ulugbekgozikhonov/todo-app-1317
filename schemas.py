from pydantic import BaseModel, Field


class AssignmentRequest(BaseModel):
	title: str = Field(min_length=3)
	priority: int = Field(gt=0, lt=6)
	description: str = Field(min_length=3, max_length=100)
	complete: bool


class CreateUserSchema(BaseModel):
	username: str
	email: str
	first_name: str
	last_name: str
	password: str
	role: str


class UserChangePassword(BaseModel):
	old_password: str
	new_password: str


class LoginSchema(BaseModel):
	username: str
	password: str
