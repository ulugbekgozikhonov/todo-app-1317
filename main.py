import uvicorn
from fastapi import FastAPI

import models
from database import engine
from routers import assignments, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TODO PROJECT")
app.include_router(assignments.router)
app.include_router(auth.router)

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=80)
