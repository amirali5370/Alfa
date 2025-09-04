from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from redis import Redis

db = SQLAlchemy()
cache = Cache()
limiter = Limiter(key_func=get_remote_address, default_limits=["60 per minute"])
