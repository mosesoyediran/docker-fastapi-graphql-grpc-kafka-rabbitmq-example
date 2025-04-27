import strawberry
from fastapi import Depends, Request, WebSocket
from strawberry.fastapi import GraphQLRouter

from config.settings import settings
from hello.db import get_db
from hello.up.mutations import Mutation as UpMutation
from hello.up.queries import Query as UpQuery
from hello.up.subscriptions import Subscription as UpSubscription


# 1) Merge Query, Mutation, Subscription via subclassing
@strawberry.type
class Query(UpQuery):
    """Combined root Query"""
    ...


@strawberry.type
class Mutation(UpMutation):
    """Combined root Mutation"""
    ...


@strawberry.type
class Subscription(UpSubscription):
    """Combined root Subscription"""
    ...


# Build the Strawberry schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)


# Make both request *and* websocket optional, so it works for HTTP & WS
async def get_context(request=None, websocket=None, db=Depends(get_db)):
    """
    Build context for both HTTP (request) and WS (websocket).
    Leaving request/websocket untyped prevents FastAPI from Pydantic-modeling them.
    """
    return {"request": request, "websocket": websocket, "db": db}


# Create the FastAPI router for GraphQL (HTTP + WebSocket)
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=settings.ENABLE_GRAPHQL,  # enable playground in ENABLE_GRAPHQL
)


