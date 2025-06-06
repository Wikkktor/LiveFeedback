from api.api_v1.routers import api_router
from db.base import Base
from db.session import engine
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from kafka.consumer import KafkaConsumerService
from elastic.utils import ensure_indices_exist

kafka_consumer: KafkaConsumerService = KafkaConsumerService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ensure_indices_exist()
    kafka_consumer.start()
    yield
    # Shutdown
    kafka_consumer.stop()


app: FastAPI = FastAPI(
    title="LiveFeedBack", version="1.0.1", debug=False, lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_router = APIRouter()
app.include_router(api_router, prefix="/api")
app.include_router(root_router)

Base.metadata.create_all(bind=engine)


@app.get("/", status_code=200)
async def root() -> dict:
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
