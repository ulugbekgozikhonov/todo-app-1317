from fastapi import APIRouter, status, HTTPException, Path

from general import db_dependency
from models import Assignment
from schemas import *

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_assignments(db: db_dependency):
	assignments = db.query(Assignment).all()
	return {"assignments": assignments}


@router.get("/{assignment_id}", status_code=status.HTTP_200_OK)
async def get_assignment_by_id(db: db_dependency, assignment_id: int = Path(gt=0)):
	assignment = db.query(Assignment).filter_by(id=assignment_id).first()
	if assignment is not None:
		return assignment
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_assignments(db: db_dependency, assignment_request: AssignmentRequest):
	assignment_model = Assignment(**assignment_request.dict())

	db.add(assignment_model)
	db.commit()


@router.put("/{assignment_id}", status_code=status.HTTP_200_OK)
async def update_assignments(db: db_dependency, assignment_request: AssignmentRequest, assignment_id: int = Path(gt=0)):
	assignment_model = db.query(Assignment).filter_by(id=assignment_id).first()
	if assignment_model is None:
		raise HTTPException(status_code=404, detail="Assignment not found")
	assignment_model.title = assignment_request.title
	assignment_model.priority = assignment_request.priority
	assignment_model.description = assignment_request.description
	assignment_model.complete = assignment_request.complete
	db.add(assignment_model)
	db.commit()


@router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
async def delete_assignments(db: db_dependency, assignment_id: int = Path(gt=0)):
	assignment_model = db.query(Assignment).filter_by(id=assignment_id).first()

	if assignment_model is None:
		raise HTTPException(status_code=404, detail="Assignment not found")

	db.query(Assignment).filter(Assignment.id == assignment_id).delete()

	db.commit()
