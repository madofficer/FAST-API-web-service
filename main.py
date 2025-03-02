import uvicorn
from fastapi import FastAPI

from routes.users_router import router_users

app = FastAPI()

# app.include_router(user_router, prefix="/user")
# app.include_router(task_router, prefix="/task")

app.include_router(router_users)



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8080,
        reload=True
    )

