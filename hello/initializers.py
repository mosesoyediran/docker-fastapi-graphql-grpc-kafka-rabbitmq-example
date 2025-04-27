from redis import Redis

from config.settings import settings

redis = Redis.from_url(str(settings.REDIS_URL))
