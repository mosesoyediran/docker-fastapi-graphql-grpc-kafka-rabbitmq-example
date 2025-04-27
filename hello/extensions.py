from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import settings

producer: AIOKafkaProducer | None = None

# Database engine and session
Base = declarative_base()
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

async def init_kafka(app: FastAPI):
    if not settings.ENABLE_KAFKA:
        return

    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()

    # keep a reference **on the app instance**
    app.state.producer = producer


async def shutdown_kafka(app: FastAPI):
    producer = getattr(app.state, "producer", None)
    if producer:
        await producer.stop()