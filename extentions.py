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
limiter = Limiter(key_func=user_or_ip)

# CACHE_TYPE = "RedisCache"               # نوع Cache
# CACHE_REDIS_URL = "redis://localhost:6379/0"  # URL Redis
# CACHE_KEY_PREFIX = "cache:"             # پیشوند برای کلیدها (اختیاری ولی توصیه شده)
# CACHE_DEFAULT_TIMEOUT = 300             # زمان پیشفرض ذخیره cache (ثانیه)
# app.config['CACHE_TYPE'] = 'RedisCache'
# app.config['CACHE_REDIS_HOST'] = 'localhost'
# app.config['CACHE_REDIS_PORT'] = 6379
# app.config['CACHE_REDIS_DB'] = 0
# app.config['CACHE_REDIS_PASSWORD'] = None  # اگر پسورد گذاشتی، اینجا بزار
# app.config['CACHE_DEFAULT_TIMEOUT'] = 300



# limiter = Limiter(
#     key_func=user_or_ip,               # تابع شناسایی کاربر (IP یا user_id)
#     storage_uri="redis://localhost:6379/1",  # Redis DB مخصوص Limiter
#     default_limits=["60 per minute"],  # محدودیت پیشفرض
#     strategy="fixed-window"            # الگوریتم شمارش محدودیت
# )

