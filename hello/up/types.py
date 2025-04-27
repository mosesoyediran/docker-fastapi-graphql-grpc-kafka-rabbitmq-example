from typing import Optional

import strawberry


@strawberry.type
class UserType:
    """
    A user record.
    """
    id: strawberry.ID
    name: str


@strawberry.type
class CreateUserPayload:
    """
    Payload returned by create_user mutation.
    """
    ok: bool
    user_id: Optional[strawberry.ID]
    message: Optional[str]
