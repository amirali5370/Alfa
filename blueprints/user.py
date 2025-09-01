from flask import Blueprint, abort, render_template, request, redirect, send_file, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from extentions import db
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError
from functions.code_generators import invite_generator, auth_generator
from scoring import *
from models.user import User
from models.invite import Invite
from models.news import News

app = Blueprint("user" , __name__)

# ------------- LOGIN AND REGISTER-------------
#register page
@app.route("/register", methods = ["POST","GET"],  strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.panel"))
    # next = request.args.get('next',None)
    inv_link = request.args.get('invite',None)
    if request.method == "POST":

        code = request.form.get('code',None)
        password = request.form.get('password',None)
        invite = request.form.get('invite',None)

        user = current_user

        invite_code = invite_generator()
        sub_invite_code = invite_generator()
        auth = auth_generator(User)

        user = User(auth=auth, first_name="کاربر", last_name="مهمان", password=sha256_crypt.encrypt(password), code=code, invite_code=invite_code, sub_invite_code=sub_invite_code, coins=coin_01)

        assistant = False
        if inv_link != None:
            invite = inv_link
        
        inviter = User.query.filter_by(invite_code=invite).first()
        if inviter == None:
            inviter = User.query.filter_by(sub_invite_code=invite).first()
            assistant = True

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            flash("unique")
            return redirect(request.url)

        if inviter != None:
                inv = Invite(inviter_id=inviter.id , invitee_id=user.id , assistant=assistant)
                inviter.coins += coin_02
                db.session.add(inv)
                db.session.commit()
        login_user(user)

        # if next != None:
        #     return redirect(next)
        return redirect(url_for("user.panel"))

    else:
        if inv_link != None:
            inviting = False
        else:
            inviting = True
        return render_template("user/register.html", inviting=inviting , current_user=current_user)
    
#is_repetitive API
@app.route('/is_repetitive', methods=['POST'])
def is_repetitive():
    data = request.get_json()
    code = data.get('code',None)
    user = User.query.filter(User.code==code).first()
    if user==None:
        result = False
    else:
        result = True
    return jsonify({'result': result})


#login page
@app.route("/login", methods = ["POST","GET"],  strict_slashes=False)
def login():
    # next = request.args.get('next',None)
    if request.method == "POST":
        code = request.form.get('code',None)
        password = request.form.get('password',None)
        user = User.query.filter(User.code==code).first()
        if user == None:
            flash("کدملی یا رمز عبور اشتباه است!")
            return redirect(request.url)      
        elif sha256_crypt.verify(password, user.password):
            login_user(user)
            # if next != None:
            #     return redirect(next)
            return redirect(url_for("user.panel"))
        else:
            flash("کدملی یا رمز عبور اشتباه است!")
            return redirect(request.url)
    else:
        return render_template("user/login.html", next=next)
    

#logout link
@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('user.home'))





#panel
@app.route("/panel")
def panel():
    return "user panel"




@app.route("/", methods = ["POST","GET"],  strict_slashes=False)
def home():
    top_users = User.query.filter(User.completion == 1).order_by(User.coins.desc()).limit(9).all()
    return render_template("home.html", current_user=current_user, top_users=top_users)




@app.route("/blog", strict_slashes=False)
def blog():
    page = request.args.get("page", 1, type=int)
    news = News.query.order_by(News.id.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("user/blog.html", current_user=current_user, news=news)


@app.route("/api/blog", strict_slashes=False)
def blog_api():
    page = request.args.get("page", 1, type=int)
    news = News.query.order_by(News.id.desc()).paginate(page=page, per_page=12, error_out=False)
    return {
        "items": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description if item.description else "",
                "url": url_for('user.single_blog', news_link=item.prima_link),
                "image": url_for('static', filename='img/news/' + str(item.auth) + '.jpg'),
                "jalali_date": item.jalali_date
            }
            for item in news.items
        ],
        "has_next": news.has_next
    }




@app.route("/blog/<news_link>",  strict_slashes=False)
def single_blog(news_link):
    news = News.query.filter_by(prima_link=news_link).first_or_404()
    return render_template("user/single_blog.html", current_user=current_user, news=news)








@app.route("/guide", methods = ["POST","GET"],  strict_slashes=False)
def guide():
    return render_template("home.html", current_user=current_user)
@app.route("/support", methods = ["POST","GET"],  strict_slashes=False)
def support():
    return render_template("home.html", current_user=current_user)

# #login page
# @app.route("/login", methods = ["POST","GET"],  strict_slashes=False)
# def login():

#     # login_user(user)
#     return "login"
