import json
from functools import lru_cache
from typing import List, Optional, Union

from pydantic import AnyUrl, PostgresDsn, RedisDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool 

    SERVER_NAME: str

    # only this is needed to talk to Postgres:
    DATABASE_URL: PostgresDsn

    SQLALCHEMY_TRACK_MODIFICATIONS: bool

    # Redis & Celery
    REDIS_URL: RedisDsn
    
    # RabbitMQ
    ENABLE_RABBITMQ: bool
    RABBITMQ_URL: Optional[AnyUrl] = None
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: bool
    
    # Toggle GraphQL support on/off
    ENABLE_GRAPHQL: bool 

    # gRPC
    ENABLE_GRPC: bool 
    GRPC_PORT: int
    ENABLE_GRPC_REFLECTION: bool 
    

    # Kafka (optional)
    ENABLE_KAFKA: bool
    KAFKA_BOOTSTRAP_SERVERS: Optional[List[str]] = None
        
    # ────────────────────────────────────────

    # If you did want JSON-decoding of KAFKA_BOOTSTRAP_SERVERS:
    @validator("KAFKA_BOOTSTRAP_SERVERS", pre=True)
    def _parse_kafka_servers(cls, v: Union[str, List[str], None]) -> Optional[List[str]]:
        if not v:
            return None
        # if they already passed a list, trust it
        if isinstance(v, list):
            return v
        # strip whitespace
        v2 = v.strip()
        # JSON array?
        if v2.startswith("[") and v2.endswith("]"):
            try:
                arr = json.loads(v2)
                if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                    return arr
            except json.JSONDecodeError:
                pass
        # fallback to comma-separated
        return [item.strip() for item in v2.split(",") if item.strip()]
    
    
    @property
    def broker_url(self) -> str:
        if self.ENABLE_RABBITMQ and self.RABBITMQ_URL:
            return str(self.RABBITMQ_URL)
        if self.ENABLE_KAFKA and self.KAFKA_BOOTSTRAP_SERVERS and self.ENABLE_RABBITMQ is False:
            # just join the list
            return "kafka://" + ",".join(self.KAFKA_BOOTSTRAP_SERVERS)
        return str(self.REDIS_URL)
    
    @property
    def CELERY_CONFIG(self) -> dict:
        return {
            "broker_url": self.broker_url,
            "result_backend": str(self.REDIS_URL),
            "include": [],
        }

    


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
