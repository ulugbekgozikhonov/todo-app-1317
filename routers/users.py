from fastapi import APIRouter, status, HTTPException
from passlib.context import CryptContext

from general import db_dependency
from models import User
from schemas import UserChangePassword

router = APIRouter(prefix="/user", tags=["user"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(db: db_dependency):
	user_model = db.query(User).filter(User.id == 1).first()
	return {"data": user_model}


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(db: db_dependency, user_request: UserChangePassword):
	user_model: User = db.query(User).filter(User.id == 1).first()

	if not bcrypt_context.verify(user_request.old_password, user_model.password):
		raise HTTPException(status_code=401, detail="Error Password change")

	user_model.password = bcrypt_context.hash(user_request.new_password)
	db.add(user_model)
	db.commit()
