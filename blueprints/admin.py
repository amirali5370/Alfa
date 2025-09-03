from flask import Blueprint, jsonify, render_template, request, send_file, session, redirect, abort, flash, url_for
from PIL import Image
from datetime import datetime , timezone
from config import ADMIN_PASSWORD, ADMIN_USERNAME
from config import STATIC_SAVE_PATH
from functions.code_generators import auth_generator
from functions.datetime import gregorian_to_jalali, jalali_to_gregorian
from extentions import db
from models.news import News
from models.pamphlet import Pamphlet
from models.question import Question
from models.quiz import Quiz

app = Blueprint("admin" , __name__ , url_prefix='/admin')

@app.before_request
def before_request():
    if session.get("admin_login", None) == None and request.endpoint != "admin.login":
        abort(404)


@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username',None)
        password = request.form.get('password',None)

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_login"] = username
            return redirect(url_for("admin.blog"))
        else:
            return redirect(url_for("admin.login"))
    else:
        return render_template("admin/login.html")


@app.route("/blog", strict_slashes=False)
def blog():
    page = request.args.get("page", 1, type=int)
    news = News.query.order_by(News.id.desc()).paginate(page=page, per_page=12, error_out=False)
    return render_template("admin/blog.html", news=news)

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
                "url": url_for('admin.single_blog', news_link=item.prima_link),
                "image": url_for('static', filename='img/news/' + str(item.auth) + '.jpg'),
                "jalali_date": item.jalali_date
            }
            for item in news.items
        ],
        "has_next": news.has_next
    }

@app.route("/blog/<news_link>", methods={"GET","POST"}, strict_slashes=False)
def single_blog(news_link):
    if news_link == "create":
        n = News(title='', description='', content='', prima_link='', auth=auth_generator(News), grade_bits=7, jalali_date=gregorian_to_jalali(datetime.now(timezone.utc)))
        db.session.add(n)
        db.session.flush()
        n.prima_link = f"news_{n.id}"
        db.session.commit()
        return render_template("admin/single_blog.html", news=n, grades=[])
    news = News.query.filter_by(prima_link=news_link).first_or_404()
    if request.method == "POST":
        mode = request.form.get('mode',None)
        if mode=="met":
            title = request.form.get('title',None)
            description = request.form.get('description',None)
            content = request.form.get('content',None)
            prima_link = request.form.get('prima_link',None)
            
            grade_bits = 0
            for i in [1, 2, 4]:
                if request.form.get(f'd{i}'):
                    grade_bits += i

            news.title = title
            news.description = description
            news.content = content
            news.prima_link = prima_link
            news.grade_bits = grade_bits
            db.session.commit()
        elif mode=="ph":
            file = request.files.get("profile", None)
            image = Image.open(file)
            image = image.resize((1600, 900))
            image = image.convert("RGB") 
            image.save(f"{STATIC_SAVE_PATH}/img/news/{news.auth}.jpg", 'JPEG')

        return redirect(url_for('admin.single_blog', news_link=news.prima_link))
    else:
        grade_bits = news.grade_bits
        return render_template("admin/single_blog.html", news=news, grades=[i for i in [1,2,4] if (i&grade_bits) !=0 ])
    

@app.route("/api/blog_del/<news_link>", strict_slashes=False)
def blog_del(news_link):
    news = News.query.filter_by(prima_link=news_link).first_or_404()
    db.session.delete(news)
    db.session.commit()
    return redirect(url_for('admin.blog'))



@app.route("/pamphlet", methods=["POST","GET"], strict_slashes=False)
def pamphlet():
    if request.method=="POST":
        pass
    else:
        pamphlets = Pamphlet.query.order_by(Pamphlet.id.desc()).all()
        return render_template("admin/pamphlet.html", pamphlets=pamphlets)


@app.route("/edit_pamphlet/<pamphlet_auth>", methods=["POST"], strict_slashes=False)
def edit_pamphlet(pamphlet_auth):
    pamphlets = Pamphlet.query.filter_by(auth=pamphlet_auth).first_or_404()
    title = request.form.get('title',None)
    description = request.form.get('description',None)    
    grade_bits = 0
    for i in [1, 2, 4]:
        if request.form.get(f'd{i}'):
            grade_bits += i

    pamphlets.title = title
    pamphlets.description = description
    pamphlets.grade_bits = grade_bits
    db.session.commit()

    return redirect(url_for('admin.pamphlet'))

@app.route("/del_pamphlet/<pamphlet_auth>", methods=["GET"], strict_slashes=False)
def del_pamphlet(pamphlet_auth):
    pamphlets = Pamphlet.query.filter_by(auth=pamphlet_auth).first_or_404()
    db.session.delete(pamphlets)
    db.session.commit()
    return redirect(url_for('admin.pamphlet'))



@app.route("/quiz", methods=["POST","GET"], strict_slashes=False)
def quiz():
    if request.method=="POST":
        pass
    else:
        items = Quiz.query.order_by(Quiz.id.desc()).all()
        past, running, upcoming = [], [], []
        now = datetime.utcnow()
        for item in items:
            if item.end_time < now:
                past.append(item)
            elif item.start_time > now:
                upcoming.append(item)
            else:
                running.append(item)

        return render_template("admin/quiz.html", past=past, running=running, upcoming=upcoming)


@app.route("/edit_quiz/<quiz_auth>", methods=["POST"], strict_slashes=False)
def edit_quiz(quiz_auth):
    
    quizes = Quiz.query.filter_by(auth=quiz_auth).first_or_404()
    status = request.form.get('status',None)
    if status=="now":
        end_jalali = request.form.get('end_jalali',None)
        quizes.end_jalali = end_jalali
        end_time = jalali_to_gregorian(end_jalali)
        quizes.end_time = end_time
    else:
        title = request.form.get('title',None)
        count = request.form.get('count',None)    
        start_jalali = request.form.get('start_jalali',None)    
        end_jalali = request.form.get('end_jalali',None)

        grade_bits = 0
        for i in [1, 2, 4]:
            if request.form.get(f'd{i}'):
                grade_bits += i

        quizes.title = title
        quizes.count = count
        quizes.start_jalali = start_jalali
        quizes.end_jalali = end_jalali
        quizes.grade_bits = grade_bits

        start_time = jalali_to_gregorian(start_jalali)
        end_time = jalali_to_gregorian(end_jalali)

        quizes.start_time = start_time
        quizes.end_time = end_time


    db.session.commit()

    return redirect(url_for('admin.quiz'))