from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_limiter import Limiter
from flask_login import current_user
# from redis import Redis

def user_or_ip():
    if current_user.is_authenticated:
        return str(current_user.id)
    return request.remote_addr

db = SQLAlchemy()
cache = Cache()
limiter = Limiter(
    key_func=user_or_ip,
    storage_uri="redis://:R1VTat2uhplNCwVnk6HAy75r5rQbU5iV@redis-17195.crce177.me-south-1-1.ec2.redns.redis-cloud.com:17195/0"
)
