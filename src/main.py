from fastapi import FastAPI

from src.user.controller import USER_SERVICE

app = FastAPI(title="Example FastAPI App")

app.include_router(USER_SERVICE, prefix="/api/users")
 


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
