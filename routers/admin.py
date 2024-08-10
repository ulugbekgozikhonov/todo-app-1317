from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Path, Depends, Query

from general import db_dependency
from models import Assignment
from schemas import *
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/assignments')
async def get_assignments(user: user_dependency, db: db_dependency):
	if user is None or user.get('role') != 'admin':
		raise HTTPException(status_code=401, detail="Authenticated failed")
	assignments = db.query(Assignment).all()
	return assignments


@router.get('/assignments/{assignment_id}')
async def get_assignment(user: user_dependency, db: db_dependency, assignment_id: int = Path(gt=0)):
	if user is None or user.get('role') != 'admin':
		raise HTTPException(status_code=401, detail="Authenticated failed")

	assignment = db.query(Assignment).filter_by(id=assignment_id)
	if assignment is not None:
		return assignment
	raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")


@router.delete('/assignments/delete/{assignment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: user_dependency, db: db_dependency, assignment_id: int = Path(gt=0)):
	if user is None or user.get('role') != 'admin':
		raise HTTPException(status_code=401, detail="Authenticated failed")
	try:
		db.query(Assignment).filter_by(id=assignment_id).delete()
		db.commit()
	except:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
