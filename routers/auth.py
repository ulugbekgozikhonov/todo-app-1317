from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt
from passlib.context import CryptContext

from general import db_dependency, tashkent
from models import User
from schemas import CreateUserSchema, LoginSchema

SECRET_KEY = "supperpuppersecretkey12345894i39asdfjasasdfjg1234589@#"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])


def authenticate_user(username: str, password: str, db: db_dependency):
	user = db.query(User).filter_by(username=username).first()
	if not user:
		return False
	if not bcrypt_context.verify(password, user.password):
		return False
	return user


def create_access_token(username: str, user_id: int, role: str):
	encode = {"sub": username, "id": user_id, 'role': role}
	expires = datetime.now(tz=tashkent) + timedelta(hours=20)
	encode.update({"exp": expires})

	return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(user_request: CreateUserSchema, db: db_dependency):
	user_model = User(
		username=user_request.username,
		first_name=user_request.first_name,
		last_name=user_request.last_name,
		email=user_request.email,
		password=bcrypt_context.hash(user_request.password),
		role=user_request.role
	)
	if user_model is None:
		raise HTTPException(status_code=400, detail="Bad Request")
	db.add(user_model)
	db.commit()


@router.post("/signin", response_model=dict)
async def get_token(form_data: Annotated[LoginSchema, Depends()], db: db_dependency):
	user: User = authenticate_user(form_data.username, form_data.password, db)
	if user is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.3")
	token = create_access_token(user.username, user.id, user.role)
	return {"access_token": token, "token_type": "bearer"}
