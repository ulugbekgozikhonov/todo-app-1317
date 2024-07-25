import uvicorn
from typing import Annotated
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from models import AssignmentModel
from schemas import *

import models
from database import engine, SessionLocal

app = FastAPI(title="TODO PROJECT")

models.Base.metadata.create_all(bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_depends = Annotated[Session, Depends(get_db)]


@app.get("/assignments", status_code=status.HTTP_200_OK)
async def get_assignments(db: db_depends):
	assignments = db.query(AssignmentModel).all()
	return {"assignments": assignments}


@app.post("/assignments/create", status_code=status.HTTP_201_CREATED)
async def create_assignments(assignment: AssignmentCreateSchema, db: db_depends):
	assignment_model = AssignmentModel(**assignment.dict())

	db.add(assignment_model)
	db.commit()


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=80)
