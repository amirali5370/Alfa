from flask import Blueprint, jsonify, render_template, request, send_file, session, redirect, abort, flash, url_for
from PIL import Image
from datetime import datetime , timezone
import pandas as pd
from werkzeug.utils import secure_filename
from pathlib import Path
from passlib.hash import sha256_crypt
from config import ADMIN_PASSWORD, ADMIN_USERNAME
from config import STATIC_SAVE_PATH
from functions.code_generators import auth_generator, invite_generator
from functions.datetime import gregorian_to_jalali, jalali_to_gregorian
from extentions import db, cache
from blueprints.user import get_all_course, get_all_quiz, get_all_webinar, get_events, get_news_page, get_news_by_link, get_pamphlet, get_parts_cached, get_quiz_and_questions
from models.course import Course
from models.news import News
from models.pamphlet import Pamphlet
from models.part import Part
from models.question import Question
from models.quiz import Quiz
from models.user import User
from models.webinar import Webinar
from models.workbook import Workbook



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
        n = News(title='', description='', content='', prima_link='', auth=auth_generator(News), grade_bits=0, jalali_date=gregorian_to_jalali(datetime.now(timezone.utc)), xml_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        db.session.add(n)
        db.session.flush()
        n.prima_link = f"news_{n.id}"
        db.session.commit()
        cache.delete_memoized(get_news_page)
        cache.delete_memoized(get_events)
        cache.delete('sitemap_xml')

        return redirect(url_for("admin.blog"))
    
    news = News.query.filter_by(prima_link=news_link).first_or_404()
    if request.method == "POST":
        news.xml_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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

        elif mode=="ph":
            file = request.files.get("profile", None)
            image = Image.open(file)
            image = image.resize((1600, 900))
            image = image.convert("RGB") 
            image.save(f"{STATIC_SAVE_PATH}/img/news/{news.auth}.jpg", 'JPEG')
            
        db.session.commit()
        cache.delete_memoized(get_news_page)
        cache.delete_memoized(get_news_by_link,news_link)
        cache.delete_memoized(get_events)
        cache.delete('sitemap_xml')

        return redirect(url_for('admin.single_blog', news_link=news.prima_link))
    else:
        grade_bits = news.grade_bits
        return render_template("admin/single_blog.html", news=news, grades=[i for i in [1,2,4] if (i&grade_bits) !=0 ])
    

@app.route("/api/blog_del/<news_link>", strict_slashes=False)
def blog_del(news_link):
    news = News.query.filter_by(prima_link=news_link).first_or_404()
    db.session.delete(news)
    db.session.commit()
    cache.delete_memoized(get_news_page)
    cache.delete_memoized(get_news_by_link,news_link)
    cache.delete_memoized(get_events)
    cache.delete('sitemap_xml')
    return redirect(url_for('admin.blog'))



@app.route("/pamphlet", methods=["POST","GET"], strict_slashes=False)
def pamphlet():
    if request.method=="POST":
        title = request.form.get('title',None)
        description = request.form.get('description',None)
        file = request.files.get('file')
        grade_bits = 0
        for i in [1, 2, 4]:
            if request.form.get(f'd{i}'):
                grade_bits += i

        pamphlets = Pamphlet(title=title, description=description, grade_bits=grade_bits, auth=auth_generator(Pamphlet))
        db.session.add(pamphlets)
        db.session.flush()
        file.save(f"{STATIC_SAVE_PATH}/files/pamphlets/{pamphlets.auth}.pdf")   
        db.session.commit()
        cache.delete_memoized(get_pamphlet)
        return redirect(request.url)
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
    cache.delete_memoized(get_pamphlet)

    return redirect(url_for('admin.pamphlet'))

@app.route("/del_pamphlet/<pamphlet_auth>", methods=["GET"], strict_slashes=False)
def del_pamphlet(pamphlet_auth):
    pamphlets = Pamphlet.query.filter_by(auth=pamphlet_auth).first_or_404()
    db.session.delete(pamphlets)
    db.session.commit()
    cache.delete_memoized(get_pamphlet)

    return redirect(url_for('admin.pamphlet'))



@app.route("/quiz", methods=["POST","GET"], strict_slashes=False)
def quiz():
    if request.method=="POST":
        title = request.form.get('title',None)
        count = request.form.get('count',None)    
        start_jalali = request.form.get('start_jalali',None)    
        end_jalali = request.form.get('end_jalali',None)

        grade_bits = 0
        for i in [1, 2, 4]:
            if request.form.get(f'd{i}'):
                grade_bits += i

        quizes = Quiz(title=title, count=count, grade_bits=grade_bits, start_jalali=start_jalali, end_jalali=end_jalali, start_time=jalali_to_gregorian(start_jalali), end_time=jalali_to_gregorian(end_jalali), auth=auth_generator(Quiz))
        db.session.add(quizes)
        db.session.commit()
        cache.delete_memoized(get_all_quiz)
        return redirect(request.url)

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
    cache.delete_memoized(get_all_quiz)
    cache.delete_memoized(get_quiz_and_questions,quiz_auth)

    return redirect(url_for('admin.quiz'))

@app.route("/del_quiz/<quiz_auth>", strict_slashes=False)
def del_quiz(quiz_auth):
    quiz = Quiz.query.filter_by(auth=quiz_auth).first_or_404()
    Question.query.filter_by(quiz_id=quiz.id).delete()

    db.session.delete(quiz)
    db.session.commit()
    cache.delete_memoized(get_all_quiz)
    cache.delete_memoized(get_quiz_and_questions,quiz_auth)

    return redirect(url_for('admin.quiz'))

@app.route("/up_quiz/<quiz_auth>", methods=["POST","GET"], strict_slashes=False)
def up_quiz(quiz_auth):
    quiz = Quiz.query.filter_by(auth=quiz_auth).first_or_404()

    file = request.files.get('quiz_file', None)
    if file!=None:
        if file.filename != '':
            df = pd.read_excel(file)
            Question.query.filter_by(quiz_id=quiz.id).delete()

            for index, row in df.iterrows():
                q = Question(quiz_id=quiz.id, text=row['text'], option_1=row['op1'], option_2=row['op2'], option_3=row['op3'], option_4=row['op4'], option_5=row['op5'])
                q.answer = q.__dict__['option_' + str(row['answer'])]
                db.session.add(q)
            
            db.session.commit()
            cache.delete_memoized(get_quiz_and_questions,quiz_auth)

    return redirect(url_for('admin.quiz'))



@app.route("/webinar", methods=["POST","GET"], strict_slashes=False)
def webinar():
    if request.method=="POST":
        title = request.form.get('title',None)
        teacher = request.form.get('teacher',None)    
        description = request.form.get('description',None)    
        content_link = request.form.get('content_link',None)    
        start_jalali = request.form.get('start_jalali',None)    
        end_jalali = request.form.get('end_jalali',None)

        grade_bits = 0
        for i in [1, 2, 4]:
            if request.form.get(f'd{i}'):
                grade_bits += i

        webinars = Webinar(title=title, description=description, teacher=teacher, content_link=content_link, grade_bits=grade_bits, start_jalali=start_jalali, end_jalali=end_jalali, start_time=jalali_to_gregorian(start_jalali), end_time=jalali_to_gregorian(end_jalali))
        db.session.add(webinars)
        db.session.commit()
        cache.delete_memoized(get_all_webinar)
        return redirect(request.url)
    else:
        items = Webinar.query.order_by(Webinar.id.desc()).all()
        past, running, upcoming = [], [], []
        now = datetime.utcnow()
        for item in items:
            if item.end_time < now:
                past.append(item)
            elif item.start_time > now:
                upcoming.append(item)
            else:
                running.append(item)
        return render_template("admin/webinar.html", past=past, running=running, upcoming=upcoming)
    
@app.route("/edit_webinar/<webinar_id>", methods=["POST"], strict_slashes=False)
def edit_webinar(webinar_id):
    
    webi = Webinar.query.filter_by(id=webinar_id).first_or_404()

    title = request.form.get('title',None)
    teacher = request.form.get('teacher',None)    
    description = request.form.get('description',None)    
    content_link = request.form.get('content_link',None)    
    start_jalali = request.form.get('start_jalali',None)    
    end_jalali = request.form.get('end_jalali',None)

    grade_bits = 0
    for i in [1, 2, 4]:
        if request.form.get(f'd{i}'):
            grade_bits += i

    webi.title = title
    webi.description = description
    webi.teacher = teacher
    webi.content_link = content_link
    webi.grade_bits = grade_bits

    webi.start_jalali = start_jalali
    webi.end_jalali = end_jalali

    start_time = jalali_to_gregorian(start_jalali)
    end_time = jalali_to_gregorian(end_jalali)

    webi.start_time = start_time
    webi.end_time = end_time

    db.session.commit()
    cache.delete_memoized(get_all_webinar)

    return redirect(url_for('admin.webinar'))


@app.route("/del_webinar/<webinar_id>", strict_slashes=False)
def del_webinar(webinar_id):
    webi = Webinar.query.filter_by(id=webinar_id).first_or_404()
    db.session.delete(webi)
    db.session.commit()
    cache.delete_memoized(get_all_webinar)
    return redirect(url_for('admin.webinar'))



@app.route("/course", methods=["POST","GET"], strict_slashes=False)
def course():
    if request.method=="POST":
        title = request.form.get('title',None)
        description = request.form.get('description',None)
        grade_bits = 0
        for i in [1, 2, 4]:
            if request.form.get(f'd{i}'):
                grade_bits += i
        cours = Course(title=title, description=description, grade_bits=grade_bits, auth=auth_generator(Course))
        db.session.add(cours)
        db.session.commit()
        cache.delete_memoized(get_all_course)

        return redirect(request.url)
    else:
        courses = Course.query.order_by(Course.id.desc()).all()
        return render_template("admin/course.html", courses=courses)
    
@app.route("/del_course/<course_auth>", strict_slashes=False)
def del_course(course_auth):
    cour = Course.query.filter_by(auth=course_auth).first_or_404()
    try:
        db.session.delete(cour)
        db.session.commit()
        cache.delete_memoized(get_all_course)
        cache.delete_memoized(get_parts_cached, course_auth)

        return redirect(url_for('admin.course'))
    except:
        return '', 204
    
@app.route("/edit_course/<course_auth>", methods=["POST","GET"], strict_slashes=False)
def edit_course(course_auth):
    cour = Course.query.filter_by(auth=course_auth).first_or_404()

    title = request.form.get('title',None)
    description = request.form.get('description',None)    

    grade_bits = 0
    for i in [1, 2, 4]:
        if request.form.get(f'd{i}'):
            grade_bits += i
    
    cour.title = title
    cour.description = description
    cour.grade_bits = grade_bits
    db.session.commit()
    cache.delete_memoized(get_all_course)
    cache.delete_memoized(get_parts_cached, course_auth)

    return redirect(url_for('admin.course'))
    


@app.route("/course/<course_auth>", methods=["POST","GET"], strict_slashes=False)
def single_course(course_auth):
    cours = Course.query.filter_by(auth=course_auth).first_or_404()
    if request.method=="POST":
        title = request.form.get('title',None)
        content_id = request.form.get('content_id',None)
        part = Part(title=title, content_id=content_id, course_id=cours.id, auth=auth_generator(Part))
        db.session.add(part)
        db.session.commit()
        cache.delete_memoized(get_parts_cached)

        return redirect(request.url)
    else:
        parts = cours.parts.all()
        return render_template("admin/part.html", cours=cours, parts=parts)
    
@app.route("/del_part/<part_auth>", strict_slashes=False)
def del_part(part_auth):
    part = Part.query.filter_by(auth=part_auth).first_or_404()
    c = part.course.auth
    db.session.delete(part)
    db.session.commit()
    cache.delete_memoized(get_parts_cached)

    return redirect(url_for('admin.single_course', course_auth=c))

    
@app.route("/edit_part/<part_auth>", methods=["POST","GET"], strict_slashes=False)
def edit_part(part_auth):
    part = Part.query.filter_by(auth=part_auth).first_or_404()
    
    title = request.form.get('title',None)
    content_id = request.form.get('content_id',None)    

    part.title = title
    part.content_id = content_id

    db.session.commit()
    cache.delete_memoized(get_parts_cached)

    c = part.course.auth

    return redirect(url_for('admin.single_course', course_auth=c))



@app.route('/dashboard')
def dashboard():
    return render_template("admin/dashboard.html")

#workbook system
@app.route('/upload-multiple', methods=['POST'])
def upload_multiple():
    files = request.files.getlist('files', None)
    title = request.form.get('title', None)
    description = request.form.get('description', None)

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            continue

        code = Path(file.filename).stem
        user = User.query.filter_by(code=code).first()
        if not user:
            return abort(403)
        auth = auth_generator(Workbook)

        file.save(f"{STATIC_SAVE_PATH}/files/workbooks/{auth}.pdf")

        w  = Workbook(user_id=user.id, is_degree=1, auth=auth, title=title, description=description)
        db.session.add(w)

    db.session.commit()
    return {'result': 'created'}, 201


#users system
@app.route('/upload-users', methods=['POST'])
def upload_users():
    file = request.files.get('file', None)


    if not file:
        return jsonify({'result': 'No files provided'}), 400

    if file.filename == '':
        return jsonify({'result': 'No files provided'}), 400
    
    typs = ['مسئول فرهنگی هنری', 'مسئول قرآنی', 'مسئول آموزشی']

    df = pd.read_excel(file, dtype={'code': str, 'password': str})

    
    for index, row in df.iterrows():
        
        invite_code = invite_generator()
        sub_invite_code = invite_generator()
        auth = auth_generator(User)

        user_type = row['user_type'] if row['user_type'] in typs else 'student'

        user = User(auth=auth, first_name=row['first_name'], last_name=row['last_name'], password=sha256_crypt.encrypt(row['password']), code=row['code'],
            user_type=user_type, province=row['province'], city=row['city'], invite_code=invite_code, sub_invite_code=sub_invite_code, coins=10)
    
        db.session.add(user)
    try:
        db.session.commit()
        return {'result': 'created'}, 201
    #اگر ارور یونیک بخوره
    except:
        db.session.rollback()
        return {'result': 'Database error'}, 500
