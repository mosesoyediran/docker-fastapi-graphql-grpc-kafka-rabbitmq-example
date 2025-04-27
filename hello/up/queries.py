from typing import List

import strawberry
from hello.up.resolvers import QueryResolver
from hello.up.types import UserType


@strawberry.type
class Query:
    """
    Root Query type.
    """

    @strawberry.field(description="A simple hello world field")
    def hello(self) -> str:
        return QueryResolver.hello(None, None)

    @strawberry.field(description="Returns all users")
    def get_users(self, info) -> List[UserType]:
        raw = QueryResolver.get_users(None, info)
        return [UserType(id=u["id"], name=u["name"]) for u in raw]