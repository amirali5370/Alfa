from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
from blueprints.general import page_not_found, ratelimit_handler
from functions.jinja_functions import *
import config
import extentions
from models.user import User
from flask_login import LoginManager

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_error_handler(404, page_not_found)
app.register_error_handler(429, ratelimit_handler)

app.jinja_env.globals['randomizer'] = randomizer
app.jinja_env.globals['and'] = lambda x, y: x & y

# ---------------- Flask Config ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.SECRET_KEY

# ---------------- Cache (Redis Cloud) ----------------
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'redis-17195.crce177.me-south-1-1.ec2.redns.redis-cloud.com'
app.config['CACHE_REDIS_PORT'] = 17195
app.config['CACHE_REDIS_PASSWORD'] = 'R1VTat2uhplNCwVnk6HAy75r5rQbU5iV'
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# ---------------- Session ----------------
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True 

Talisman(app, content_security_policy=None)

# ---------------- Extensions ----------------
extentions.db.init_app(app)
extentions.cache.init_app(app)
extentions.limiter.init_app(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()


with app.app_context():
    extentions.db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
