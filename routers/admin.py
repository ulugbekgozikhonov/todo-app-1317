from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Path, Depends

from general import db_dependency
from models import Assignment

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get('/assignments')
async def get_assignments(db: db_dependency):
	assignments = db.query(Assignment).all()
	return assignments


@router.get('/assignments/{assignment_id}')
async def get_assignment(db: db_dependency, assignment_id: int = Path(gt=0)):
	assignment = db.query(Assignment).filter_by(id=assignment_id)
	if assignment is not None:
		return assignment
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")


@router.delete('/assignments/delete/{assignment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: db_dependency, assignment_id: int = Path(gt=0)):
	try:
		db.query(Assignment).filter_by(id=assignment_id).delete()
		db.commit()
	except Exception:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
