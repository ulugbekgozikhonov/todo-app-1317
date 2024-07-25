from pydantic import BaseModel, Field


class AssignmentCreateSchema(BaseModel):
	title: str = Field(min_length=3)
	priority: int = Field(gt=0, lt=6)
	description: str
