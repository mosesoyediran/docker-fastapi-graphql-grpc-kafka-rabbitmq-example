from typing import AsyncGenerator

import strawberry
from hello.up.resolvers import SubscriptionResolver


@strawberry.type
class Subscription:
    """
    Root Subscription type.
    """

    @strawberry.subscription(description="Yields the current UNIX timestamp every second")
    async def time_ticks(self, info) -> AsyncGenerator[int, None]:

        """
        Subscription to send a timestamp every second.
        """
        async for _ in SubscriptionResolver.time_ticks_source(None, info):
            yield SubscriptionResolver.time_ticks_resolver(None, info)
