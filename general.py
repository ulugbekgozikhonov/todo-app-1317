import time

from fastapi import Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database import SessionLocal
from pytz import timezone
from jose import jwt, JWTError

SECRET_KEY = "supperpuppersecretkey12345894i39asdfjasasdfjg1234589@#"
ALGORITHM = "HS256"

tashkent = timezone("Asia/Tashkent")


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def decode_jwt(token: str) -> dict:
	try:
		decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return decoded_token if decoded_token["exp"] >= time.time() else None
	except:
		return {}


class JWTBearer(HTTPBearer):
	def __init__(self, auto_error: bool = True):
		super(JWTBearer, self).__init__(auto_error=auto_error)

	async def __call__(self, request: Request):
		credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
		if credentials:
			if not credentials.scheme == "Bearer":
				raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
			if not self.verify_jwt(credentials.credentials):
				raise HTTPException(status_code=403, detail="Invalid token or expired token.")
			return credentials.credentials
		else:
			raise HTTPException(status_code=403, detail="Invalid authorization code.")

	def verify_jwt(self, jwtoken: str) -> bool:
		isTokenValid: bool = False

		try:
			payload = decode_jwt(jwtoken)
		except:
			payload = None
		if payload:
			isTokenValid = True

		return isTokenValid
