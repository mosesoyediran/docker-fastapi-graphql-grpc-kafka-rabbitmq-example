import asyncio
import time

from hello.up.models import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class QueryResolver:
    """
    Collection of query resolvers.
    Each static method implements one field on your Query type.
    """

    @staticmethod
    def hello(parent, info) -> str:
        """
        Resolve the `hello` field.

        Returns:
            A greeting string.
        """
        return "Hello from Strawberry resolver!"

    @staticmethod
    def get_users(parent, info) -> list[dict]:
        """
        Resolve the `get_users` field.

        Args:
            parent: Not used.
            info: GraphQL execution info; info.context["db"] is a Session.

        Returns:
            A list of dicts matching UserType (keys: id, name).
        """
        db = info.context["db"]
        users = db.query(User).all()
        return [{"id": str(u.id), "name": u.name} for u in users]


class MutationResolver:
    """
    Collection of mutation resolvers.
    Each static method implements one field on your Mutation type.
    """

    @staticmethod
    def create_user(parent, info, name: str) -> dict:
        """
        Resolve the `create_user` mutation.

        Inserts a user into the database. On error rolls back.

        Args:
            parent: Not used.
            info: GraphQL execution info; info.context["db"] is a Session.
            name: the new user's name.

        Returns:
            A dict matching CreateUserPayload (keys: ok, user_id, message).
        """
        db: Session = info.context["db"]
        try:
            new_user = User(name=name)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "ok": True,
                "user_id": str(new_user.id),
                "message": f"User '{name}' created successfully.",
            }
        except SQLAlchemyError:
            db.rollback()
            return {
                "ok": False,
                "user_id": None,
                "message": "Unable to create user at this time. Please try again later.",
            }
        finally:
            db.close()


class SubscriptionResolver:
    """
    Collection of subscription resolvers.
    Each method decorated by Strawberry.subscription returns an async generator.
    """

    @staticmethod
    async def time_ticks_source(parent, info):
        """
        Generate an event every second for `time_ticks`.
        """
        while True:
            await asyncio.sleep(1)
            yield {}

    @staticmethod
    def time_ticks_resolver(parent, info) -> int:
        """
        Resolve one tick into the current UNIX timestamp.
        """
        return int(time.time())
