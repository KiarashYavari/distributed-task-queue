from fastapi import FastAPI
from api.process import router 

app = FastAPI(
    title="Worker Service",
    description="Processes tasks internally",
    version="1.0.0"
)

app.include_router(router)
