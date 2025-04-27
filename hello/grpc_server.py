# hello/grpc_server.py
import asyncio
import logging

import grpc
from grpc import aio
from grpc_reflection.v1alpha import reflection
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.settings import settings
from hello.central import user_service_pb2, user_service_pb2_grpc
from hello.extensions import SessionLocal

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    """
    gRPC servicer implementing the UserService defined in user_service.proto.
    """

    async def Hello(self, request, context) -> user_service_pb2.HelloReply:
        """
        Simple hello RPC.
        """
        return user_service_pb2.HelloReply(message="Hello from gRPC!")

    async def ListUsers(self, request, context) -> user_service_pb2.ListUsersReply:
        """
        Fetches all users from the database.
        Runs the synchronous DB call in a threadpool executor.
        """
        loop = asyncio.get_event_loop()
        rows = await loop.run_in_executor(None, self._sync_list_users)
        users = [
            user_service_pb2.User(id=str(r.id), name=r.name) for r in rows
        ]
        return user_service_pb2.ListUsersReply(users=users)

    def _sync_list_users(self):
        db = SessionLocal()
        try:
            return db.execute(
                text("SELECT id, name FROM users")
            ).all()
        finally:
            db.close()

    async def CreateUser(
        self, request, context
    ) -> user_service_pb2.CreateUserReply:
        """
        Inserts a new user with the given name.
        Returns a CreateUserReply with ok, user_id and message.
        """
        loop = asyncio.get_event_loop()
        ok, user_id, msg = await loop.run_in_executor(
            None, self._sync_create_user, request.name
        )
        return user_service_pb2.CreateUserReply(
            ok=ok, user_id=user_id or "", message=msg
        )

    def _sync_create_user(self, name: str):
        db = SessionLocal()
        try:
            result = db.execute(
                text(
                    "INSERT INTO users (name) VALUES (:name) RETURNING id"
                ),
                {"name": name},
            )
            new_id = result.scalar_one()
            db.commit()
            return True, str(new_id), f"User '{name}' created successfully."
        except SQLAlchemyError as e:
            db.rollback()
            logger.error("CreateUser failed", exc_info=e)
            return False, None, "Unable to create user at this time."
        finally:
            db.close()


async def serve():
    """
    Start up the gRPC server, listening on settings.GRPC_PORT.
    Reflection is only enabled if ENABLE_GRPC_REFLECTION is True.
    """
    server = aio.server()
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )

    # Conditionally wire up reflection
    if settings.ENABLE_GRPC_REFLECTION:
        svc_name = user_service_pb2.DESCRIPTOR.services_by_name["UserService"].full_name
        reflection.enable_server_reflection(
            [svc_name, reflection.SERVICE_NAME],
            server,
        )
        logger.info("gRPC reflection ENABLED")
    else:
        logger.info("gRPC reflection DISABLED")

    listen_addr = f"[::]:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    logger.info(f"gRPC server listening on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    if settings.ENABLE_GRPC:
        asyncio.run(serve())
    else:
        logger.warning("gRPC server disabled (ENABLE_GRPC=false)")
