from flask import Flask
from flask_wtf.csrf import CSRFProtect
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
# from blueprints.general import page_not_found
import config
import extentions
from models.user import User
from flask_login import LoginManager


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
# app.register_error_handler(404, page_not_found)

# app.jinja_env.globals['len'] = len


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.SECRET_KEY

extentions.db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id==user_id).first()



with app.app_context():
    extentions.db.create_all()



if __name__ == "__main__":
    app.run(debug= True)