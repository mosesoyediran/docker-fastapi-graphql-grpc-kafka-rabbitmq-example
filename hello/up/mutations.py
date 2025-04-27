
import strawberry
from hello.up.resolvers import MutationResolver
from hello.up.types import CreateUserPayload


@strawberry.type
class Mutation:
    """
    Root Mutation type.
    """

    @strawberry.mutation(description="Create a new user")
    def create_user(self, info, name: str) -> CreateUserPayload:
        payload = MutationResolver.create_user(None, info, name)
        return CreateUserPayload(
            ok=payload["ok"],
            user_id=payload["user_id"],
            message=payload["message"],
        )