import uvicorn
from fastapi import FastAPI
from app.user import user_route

app = FastAPI(
    title="Ping",
    docs_url="/"
)

app.include_router(router=user_route)

if __name__=="__main__":
    uvicorn.run(app=app)