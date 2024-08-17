import uvicorn
from fastapi import FastAPI

import models
from database import engine
from routers import assignments, auth, admin, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODO PROJECT")
app.include_router(assignments.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=80)
