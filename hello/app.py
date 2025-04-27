# hello/app.py

from celery import Celery, Task
from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from config.settings import settings
from hello.central.schema import graphql_app
from hello.extensions import (Base, SessionLocal, engine, init_kafka,
                              shutdown_kafka)
from hello.utils.views import router


def create_app() -> FastAPI:
    """
    Create a FastAPI application using the app factory pattern.
    """
    app = FastAPI(
        title="Hello",
        debug=settings.DEBUG,
    )

    middleware(app)
    register_extensions(app)
    register_routers(app)
    
    return app


def create_celery_app(app: FastAPI = None) -> Celery:
    """
    Create a new Celery app and tie together the Celery config to the app's config.
    """
    app = app or create_app()

    class FastAPITask(Task):
        def __call__(self, *args, **kwargs):
            return self.run(*args, **kwargs)

    celery = Celery(__name__, task_cls=FastAPITask)
    celery.conf.update(settings.CELERY_CONFIG)
    celery.set_default()
    app.state.celery = celery

    return celery


def register_extensions(app: FastAPI):
    """
    Tie the SQLAlchemy engine and session into FastAPI:
    - Store in app.state
    - Test DB connection on startup
    - Dispose engine on shutdown
    """
    app.state.engine = engine
    app.state.SessionLocal = SessionLocal

    @app.on_event("startup")
    async def _startup():
        Base.metadata.create_all(bind=engine)
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")

    @app.on_event("shutdown")
    async def shutdown():
        engine.dispose()
        
    @app.on_event("startup")
    async def _startup_kafka():
        if settings.ENABLE_KAFKA:
            await init_kafka(app)
    
    @app.on_event("shutdown")
    async def _shutdown_kafka():
        if settings.ENABLE_KAFKA:
            await shutdown_kafka(app) 
        

    return None


def middleware(app: FastAPI):
    """
    Register middleware.
    """
    app.add_middleware(TrustedHostMiddleware)
    return None


def register_routers(app: FastAPI):
    """
    Conditionally register the Strawberry GraphQL router at /graphql,
    or expose a simple JSON health check at /graphql when GraphQL is disabled.
    """
    if settings.ENABLE_GRAPHQL:
        # HTTP + WS GraphQL endpoint
        app.include_router(graphql_app, prefix="/graphql")
    else:
        # Map both /graphql and /graphql/ to our health check
        @app.get("/graphql", tags=["health"])
        @app.get("/graphql/", tags=["health"])
        def graphql_disabled_health():
            return {"status": "ok", "graphql": "disabled"}
    
    app.include_router(router) 

    return None



# Entrypoints
app = create_app()
celery_app = create_celery_app(app)
