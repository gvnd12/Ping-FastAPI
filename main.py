import uvicorn
from fastapi import FastAPI
from app.api import user_route, auth_route

app = FastAPI(
    title="Ping",
    docs_url="/"
)

app.include_router(router=auth_route)
app.include_router(router=user_route)

if __name__=="__main__":
    uvicorn.run(app=app)