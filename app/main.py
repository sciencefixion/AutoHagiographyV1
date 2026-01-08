from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from app.routers import users, journals, posts

app = FastAPI()

origins = ["http://localhost"]

# TODO CORS middleware setup

#Global custom exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"message":f"{exception.detail}"}
    )

# Import routers
app.include_router(users.router)
app.include_router(journals.router)
app.include_router(posts.router)

@app.get("/")
async def read_root():
    return {"message":"Welcome to AutoHagiography!"}