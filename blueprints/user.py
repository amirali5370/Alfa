from flask import Blueprint, Response, abort, render_template, request, redirect, send_file, send_from_directory, url_for, flash, jsonify, g
from flask_login import login_user, login_required, current_user, logout_user
from flask_limiter import Limiter
from extentions import db, cache, limiter
from functions.give_city_data import cities as city_data
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import requests
from sqlalchemy import literal
from sqlalchemy.sql import exists
from PIL import Image
import os
import random
from functions.code_generators import invite_generator, auth_generator
from config import CHAT_ID, PAY_API, PRICE, STATIC_SAVE_PATH, TOKEN, URL_PAY_TOKEN, URL_PAY_VERIFY, VID_API_KEY, VID_SECRET_KEY
from functions.datetime import gregorian_to_jalali
from models.reservation import Reservation
from scoring import *
from models.user import User
from models.invite import Invite
from models.news import News
from models.ticket import Ticket
from models.quiz import Quiz
from models.workbook import Workbook
from models.pamphlet import Pamphlet
from models.webinar import Webinar
from models.course import Course
from models.result import Result
from models.question import Question
from models.payment import Payment
from models.camp import Camp
from models.part import Part



app = Blueprint("user" , __name__)

#temporary
#موقت
@app.route("/modiran", methods=["GET"], strict_slashes=False)
def modiran_porsline():
    return redirect('https://survey.porsline.ir/s/oYVie60h')

# nonce system
# تولید nonce برای هر درخواست
# @app.before_request
# def generate_nonce():
#     # 16 بایت تصادفی -> hex string
#     g.nonce = os.urandom(16).hex()

# inject nonce به تمام تمپلیت‌ها تا لازم نباشه دستی پاس بدیم
# @app.context_processor
# def inject_nonce():
#     return dict(nonce=getattr(g, 'nonce', ''))

# اضافه کردن هدر CSP به پاسخ‌های HTML
# @app.after_request
# def add_csp_header(response):
#     nonce = getattr(g, 'nonce', None)
#     content_type = response.headers.get('Content-Type', '')
#     # فقط برای پاسخ‌های HTML هدر CSP بگذار
#     if nonce and 'text/html' in content_type:
#         csp = (
#             "default-src 'self'; "
#             f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
#             f"style-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
#             "img-src 'self' data: https://cdn.jsdelivr.net; "
#             "font-src 'self' https://cdn.jsdelivr.net; "
#             "object-src 'none'; "
#             "base-uri 'self';"
#         )
#         response.headers['Content-Security-Policy'] = csp
#     return response


# ------------- site map -------------
def get_posts_xml():
    return News.query.all()

@cache.cached(key_prefix='sitemap_xml', timeout=0)
@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    pages = []

    # صفحات ثابت
    pages.append({
        "loc": url_for('user.home', _external=True),
        "lastmod": "2025-09-22"
    })
    pages.append({
        "loc": url_for('user.blog', _external=True),
        "lastmod": "2025-09-22"
    })
    pages.append({
        "loc": url_for('user.guide', _external=True),
        "lastmod": "2025-09-22"
    })
    pages.append({
        "loc": url_for('user.support', _external=True),
        "lastmod": "2025-09-22"
    })

    # صفحات سینگل بلاگ
    for post in get_posts_xml():
        pages.append({
            "loc": url_for('user.single_blog', news_link=post.prima_link, _external=True),
            "lastmod": post.xml_date
        })

    # تولید XML
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("  <url>")
        xml.append(f"    <loc>{page['loc']}</loc>")
        xml.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        xml.append("    <changefreq>weekly</changefreq>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")
    sitemap_xml = "\n".join(xml)
    return Response(sitemap_xml, mimetype='application/xml')


@app.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")



# ------------- LOGIN AND REGISTER-------------
#register page
@app.route("/register", methods = ["POST","GET"],  strict_slashes=False)
# @limiter.limit("3 per hour")
def register():
    if current_user.is_authenticated:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    
    next = request.args.get('next',None)
    inv_link = request.args.get('invite',None)
    if request.method == "POST":

        code = request.form.get('code',None)
        password = request.form.get('password',None)
        invite = request.form.get('invite',None)

        province = request.form.get('province',None)
        city = request.form.get('city',None)

        user = current_user

        invite_code = invite_generator()
        sub_invite_code = invite_generator()
        auth = auth_generator(User)

        user = User(auth=auth, first_name="کاربر", last_name="مهمان", password=sha256_crypt.encrypt(password), code=code, invite_code=invite_code, sub_invite_code=sub_invite_code, coins=coin_01, province=province, city=city)

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
            db.session.rollback()
            flash("unique")
            return redirect(request.url)

        if inviter != None:
            inv = Invite(inviter_id=inviter.id , invitee_id=user.id, assistant=assistant)
            inviter.coins += coin_02
            db.session.add(inv)
            if assistant:
                user.user_type="M"+inviter.user_type
            db.session.commit()
        login_user(user)

        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    else:
        if inv_link != None:
            inviting = False
        else:
            inviting = True
        return render_template("user/register.html", inviting=inviting, current_user=current_user, next=next, provinces=city_data.keys())
    

#is_repetitive API
@app.route('/is_repetitive', methods=['POST'])
@limiter.limit("10 per hour")
def is_repetitive():
    data = request.get_json()
    code = data.get('code',None)
    user = User.query.filter(User.code==code).first()
    if user==None:
        result = False
    else:
        result = True
    return jsonify({'result': result})

#get city api
@app.route('/get_cities')
def get_cities():
    province = request.args.get('province' , None)
    if province == None:
        abort(404)
    cities = city_data.get(province, [])
    return jsonify(cities)


#login page
@app.route("/login", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("10 per minute")
def login():
    next = request.args.get('next',None)
    if current_user.is_authenticated:
        if next != None:
            return redirect(next)
        return redirect(url_for("user.dashboard"))
    
    if request.method == "POST":
        code = request.form.get('code',None)
        password = request.form.get('password',None)
        user = User.query.filter(User.code==code).first()
        if user == None:
            flash("کدملی یا رمز عبور اشتباه است!")
            return redirect(request.url)      
        elif sha256_crypt.verify(password, user.password):
            login_user(user)
            if next != None:
                return redirect(next)
            return redirect(url_for("user.dashboard"))
        else:
            flash("کدملی یا رمز عبور اشتباه است!")
            return redirect(request.url)
    else:
        return render_template("user/login.html", next=next)
    

#logout link
@app.route("/logout")
@limiter.limit("5 per minute")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('user.home'))



#top users caching
@cache.memoize(timeout=3600)
def get_top_users():
    return User.query.filter(User.completion == 1, User.pay == 1).order_by(User.coins.desc()).limit(9).all()

@app.route("/",  strict_slashes=False)
@limiter.limit("60 per minute")
def home():
    top_users = get_top_users()
    return render_template("home.html", current_user=current_user, top_users=top_users)



# news system
@cache.memoize(timeout=0)
def get_news_page(page):
    pagination = News.query.order_by(News.id.desc()).paginate(page=page, per_page=12, error_out=False)
    return pagination.items, pagination.has_next, pagination.page

@cache.memoize(timeout=0)
def get_news_by_link(link):
    return News.query.filter_by(prima_link=link).first_or_404()


@app.route("/blog", strict_slashes=False)
@limiter.limit("60 per minute")
def blog():
    page = request.args.get("page", 1, type=int)
    news, has, news_page = get_news_page(page)
    return render_template("user/blog.html", current_user=current_user, news=news, has_next=has, page=news_page)


@app.route("/api/blog", strict_slashes=False)
@limiter.limit("200 per minute")
def blog_api():
    page = request.args.get("page", 1, type=int)
    news, has, page = get_news_page(page)
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
            for item in news
        ],
        "has_next": has
    }


@app.route("/blog/<news_link>", strict_slashes=False)
def single_blog(news_link):
    news = get_news_by_link(news_link)
    return render_template("user/single_blog.html", current_user=current_user, news=news)




@app.route("/guide", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("6 per minute")
def guide():
    return render_template("user/guide.html", current_user=current_user)

@app.route("/support", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("3 per minute")
def support():
    if request.method == "POST":
        name = request.form.get('name',None)
        code = request.form.get('code',None)
        phone = request.form.get('phone',None)
        message = request.form.get('message',None)
        try:
            TEXT = f"""
            نام و نام خانوادگی : {name}
        کدملی : {code}
        شماره تلفن : {phone}

        متن پیام:
        {message}
            """

            url = (f"https://eitaayar.ir/api/{TOKEN}/sendMessage")
            data = {"UrlBox":url,
                        "chat_id": CHAT_ID,
                        "text":TEXT        
            }
            req = requests.post(url=url,data=data)
            if bool(req.json()['ok']) == True:
                tick = Ticket(name=name, code=code, phone=phone, message=message, jalali_date=gregorian_to_jalali(datetime.now(timezone.utc)))
                db.session.add(tick)
                db.session.commit()
                flash("ticket_add_success")
            else:
                flash("ticket_add_error")


        except:
            db.session.rollback()
            flash("ticket_add_error")

        return redirect(request.url)
    else:
        return render_template("user/support.html", current_user=current_user)





#dashboard
@app.route("/dashboard", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("30 per minute")
@login_required
def dashboard():
    if request.method == "POST":
        current_user.first_name = request.form.get('first_name',None)
        current_user.last_name = request.form.get('last_name',None)
        current_user.father_name = request.form.get('father_name',None)
        current_user.gender = request.form.get('gender',None)
        current_user.school_name = request.form.get('school_name',None)
        current_user.number = request.form.get('number',None)
        current_user.addres = request.form.get('addres',None)

        grade = int(request.form.get('grade',None))
        current_user.grade = grade
        grade_dist ={
            4: "چهارم",
            5: "پنجم",
            6: "ششم",
            7: "هفتم",
            8: "هشتم",
            9: "نهم",
            10: "دهم",
            11: "یازدهم",
            12: "دوزادهم"
        }
        current_user.grade_name = grade_dist[grade]
        current_user.period_code = 2**((grade-1)//3 - 1)

        current_user.completion = 1
        try:
            db.session.commit()
            flash("completion_success")
        except:
            db.session.rollback()
        return redirect(request.url)
    else:
        sub_invits = current_user.sent_invitations.filter_by(assistant=1).all()
        return render_template("user/dashboard.html", current_user=current_user, sub_invits=sub_invits)
    
#switch_sub API
@app.route('/api/switch_sub', methods=['POST','GET'])
@limiter.limit("60 per minute")
def switch_sub():
    if not(current_user.is_authenticated) or current_user.completion == 0 or current_user.pay == 0 :
        return abort(404)
    
    data = request.get_json()
    invite_id = data.get('invite_id', None)
    do = data.get('do', None)
    if do == "activate":
        if Invite.query.filter(Invite.inviter_id == current_user.id, Invite.assistant==1, Invite.activate==1).count() >= 3:
            return jsonify({'result': "403"})

    inv = Invite.query.filter(Invite.id == invite_id, Invite.inviter_id == current_user.id, Invite.assistant==1).first_or_404()

    try:
        inv.activate = int(not inv.activate)
        db.session.commit()
        result = "200"
    except:
        result = "500"

    return jsonify({'result': result})

@app.route("/account", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("30 per minute")
@login_required
def account():
    if request.method == "POST":
        _type = request.form.get('type', None)
        if _type == "psw":
            now_pass = request.form.get('now_pass', None)
            new_pass = request.form.get('new_pass', None)
            if sha256_crypt.verify(now_pass, current_user.password):
                current_user.password = sha256_crypt.encrypt(new_pass)
                db.session.commit()
                flash("pass_success")
            else:
                flash("now_pass_error")
        else:
            file = request.files.get("profile", None)
            image = Image.open(file)
            image = image.resize((256, 256))
            image = image.convert("RGB") 
            image.save(f"{STATIC_SAVE_PATH}/img/users/{current_user.auth}.jpg", 'JPEG')
        return redirect(request.url)

    else:
        user_type = current_user.user_type
        if user_type == "student":
            user_type="ساده"
        elif user_type.startswith("M"):
            user_type="معاونت " + user_type[1:]

        return render_template("user/account.html", current_user=current_user, user_type=user_type)
    

@app.route("/workbook",  strict_slashes=False)
@limiter.limit("20 per minute")
@login_required
def workbook():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    workbooks = Workbook.query.filter(Workbook.user_id==current_user.id).order_by(Workbook.id.desc()).all()
    return render_template("user/workbook.html", current_user=current_user, workbooks=workbooks)

#books' file
@app.route('/download/workbook/<workbook_auth>')
@limiter.limit("20 per minute")
@login_required
def single_workbook(workbook_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return abort(404)
    Workbook.query.filter(Workbook.auth==workbook_auth, Workbook.user_id==current_user.id).first()
    path = f"{STATIC_SAVE_PATH}/files/workbooks/{workbook_auth}.pdf"
    try:
        return send_file(path, as_attachment=True)
    except:
        return abort(403)
    


# events system
@cache.memoize(timeout=0)
def get_events(pr_code):
    return News.query.filter((News.grade_bits.op('&')(literal(pr_code))) != 0).order_by(News.id.desc()).all()

@app.route("/event",  strict_slashes=False)
@limiter.limit("30 per minute")
@login_required
def event():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    events = get_events(current_user.period_code)
    return render_template("user/event.html", current_user=current_user, events=events)




# pamphlets system
@cache.memoize(timeout=0)
def get_pamphlet(pr_code):
    return Pamphlet.query.filter((Pamphlet.grade_bits.op('&')(literal(pr_code))) != 0).order_by(Pamphlet.id.desc()).all()

@app.route("/pamphlet",  strict_slashes=False)
@limiter.limit("40 per minute")
@login_required
def pamphlet():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    pamphlets = get_pamphlet(current_user.period_code)
    return render_template("user/pamphlet.html", current_user=current_user, pamphlets=pamphlets)

@app.route('/download/pamphlet/<pamphlet_auth>')
@limiter.limit("30 per minute")
@login_required
def single_pamphlet(pamphlet_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return abort(404)
    pam = Pamphlet.query.filter(Pamphlet.auth==pamphlet_auth , (Pamphlet.grade_bits.op('&')(literal(current_user.period_code))) != 0).first()
    path = f"{STATIC_SAVE_PATH}/files/pamphlets/{pam.auth}.pdf"
    try:
        return send_file(path, as_attachment=True, download_name=f"{pam.title}.pdf")
    except:
        return abort(404)
    

# quiz system
@cache.memoize(timeout=59)
def get_all_quiz(pr_code):
    return Quiz.query.filter((Quiz.grade_bits.op('&')(literal(pr_code))) != 0).order_by(Quiz.id.desc()).all()

@cache.memoize(timeout=0)
def get_quiz_and_questions(quiz_auth):
    quiz = Quiz.query.filter(Quiz.auth==quiz_auth).first()
    if not quiz:
        return abort(404)
    questions=quiz.questions.all()
    return quiz, questions


@app.route("/quiz",  strict_slashes=False)
@limiter.limit("100 per minute")
@login_required
def quiz():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    items = get_all_quiz(current_user.period_code)
    past, running, upcoming = [], [], []
    now = datetime.utcnow()
    for item in items:
        if item.end_time < now:
            past.append(item)
        elif item.start_time > now:
            upcoming.append(item)
        else:
            running.append(item)

    return render_template("user/quiz.html", current_user=current_user, past=past, running=running, upcoming=upcoming)


@app.route("/quiz/<quiz_auth>", methods = ["POST","GET"],  strict_slashes=False)
@limiter.limit("20 per minute")
@login_required
def single_quiz(quiz_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    
    quiz, all_questions = get_quiz_and_questions(quiz_auth,current_user.period_code)
    if (quiz.grade_bits & current_user.period_code) == 0:
        return abort(404)
    
    now = datetime.utcnow()
    if quiz.end_time < now or quiz.start_time > now:
        return abort(404)
    
    r = Result.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).first()
    if request.method == "POST":
        true = 0
        questions = {q.id: q for q in all_questions}
        for key, value in request.form.items():
            if key.startswith("q"):
                q = questions.get(int(key[1:]))
                if not q:
                    continue
                if q.answer == value:
                    true += 3
                else:
                    true -= 1
                
        result = round( (true*100)/(3*quiz.count) ,2)
        if r.score < result:
            current_user.coins += round(coin_03 * (result - r.score))
            r.score = result
            try:
                db.session.commit()
            except:
                db.session.rollback()

        flash('quiz_success')
        return redirect(url_for('user.quiz'))

    else:
        if r==None:
            r = Result(user_id=current_user.id, quiz_id=quiz.id)
            db.session.add(r)
            db.session.commit()

        if r.enter > 2:
            flash('quiz_more_3')
            return redirect(url_for('user.quiz')) 
        r.enter = r.enter+1
        db.session.commit()
        questions = random.sample(all_questions, quiz.count)
        return render_template("user/single_quiz.html", quiz=quiz, questions=questions)


@app.route("/api/result", methods = ["POST","GET"], strict_slashes=False)
@limiter.limit("30 per minute")
@login_required
def result():
    if current_user.completion == 0 or current_user.pay == 0:
        return abort(404)
    data = request.get_json()
    quiz_id = int(data.get('quiz_id',None))

    r = Result.query.filter(Result.user_id==current_user.id, Result.quiz_id==quiz_id).first()

    return jsonify({'result': r.score if r != None else 0})



# webinar system
@cache.memoize(timeout=0)
def get_all_webinar(pr_code):
    return Webinar.query.filter((Webinar.grade_bits.op('&')(literal(pr_code))) != 0).order_by(Webinar.start_time).all()


@app.route("/webinar",  strict_slashes=False)
@limiter.limit("40 per minute")
@login_required
def webinar():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    items = get_all_webinar(current_user.period_code)
    past, running, upcoming = [], [], []
    now = datetime.utcnow()
    for item in items:
        if item.end_time < now:
            past.append(item)
        elif item.start_time > now:
            upcoming.append(item)
        else:
            running.append(item)

    return render_template("user/webinar.html", current_user=current_user, past=past, running=running, upcoming=upcoming)



# course system
@cache.memoize(timeout=0)
def get_all_course(pr_code):
    return Course.query.filter((Course.grade_bits.op('&')(literal(pr_code))) != 0).order_by(Course.id.desc()).all()

@cache.memoize(timeout=0)
def get_parts_cached(course_auth):
    cour = Course.query.filter(Course.auth==course_auth).first_or_404()
    part = cour.parts.all()
    return cour, part



@app.route("/course",  strict_slashes=False)
@limiter.limit("100 per minute")
@login_required
def course():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    courses = get_all_course(current_user.period_code)

    return render_template("user/course.html", courses=courses)

@app.route("/api_part", methods=["POST","GET"], strict_slashes=False)
@limiter.limit("60 per minute")
@login_required
def get_part():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        data = request.get_json()
        course_auth = data.get('course_auth',None)
        cour, part = get_parts_cached(course_auth)
        if (cour.grade_bits & current_user.period_code) == 0:
            return abort(404)
        
        return jsonify({
                "items": [
                    {
                        "title": item.title,
                        "auth": item.auth
                    }
                    for item in part
                ]
            })
    else:
        return abort(403)


@app.route("/part/<part_auth>", methods=["GET"], strict_slashes=False)
@limiter.limit("100 per minute")
@login_required
def part(part_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    p = Part.query.filter_by(auth=part_auth).first_or_404()
    url = 'https://api.vidprotect.ir/v1/storage/bucket/file/generate/link'
    headers = {
        'api_key': VID_API_KEY,
        'secret_key': VID_SECRET_KEY
    }
    payload = {
        'fileId': p.content_id,
        'mobileNumber': current_user.code
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return render_template("user/part.html", video_url=data['url'])
    except requests.exceptions.RequestException as e:
        return 'Error:'+str(e)




#camps system
@cache.memoize(timeout=0)
def get_grade_camps(pr_code):
    return Camp.query.filter((Camp.grade_bits.op('&')(literal(pr_code))) != 0)


def get_user_camps(pr_code,us_id):
    reg = get_grade_camps(pr_code).join(Reservation).filter(Reservation.user_id == us_id).all()
    sta = get_grade_camps(pr_code).filter(~exists().where((Reservation.camp_id == Camp.id) &(Reservation.user_id == us_id)), Camp.status==1).all()
    return reg,sta


@app.route("/camp", methods=["GET","POST"], strict_slashes=False)
@limiter.limit("30 per minute")
@login_required
def camp():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    if request.method == "POST":
        auth = request.get_json().get('auth', None)
        my_camp = Camp.query.filter_by(auth=auth).first_or_404()
        if Reservation.query.filter(Reservation.camp_id==my_camp.id, Reservation.user_id==current_user.id).first()!=None:
            return abort(404)
        if current_user.coins >= my_camp.price:
            r = Reservation(camp_id=my_camp.id,user_id=current_user.id)
            current_user.coins = current_user.coins - my_camp.price
            db.session.add(r)
            db.session.commit()
            return jsonify({'result':'buy'})
        else:
            return jsonify({'result':'little'})

    else:
        reg, sta = get_user_camps(pr_code=current_user.period_code, us_id=current_user.id)
        return render_template("user/camp.html", reg=reg, sta=sta)




#pay system
#payment handler
@app.route("/payment", methods=["GET","POST"])
@limiter.limit("5 per minute")
@login_required
def payment():
    if request.method=="GET":
        if current_user.pay != 0:
            return redirect(url_for("user.dashboard"))
    amount = PRICE
    inApp = 0
    if request.method=="POST":
        coins = request.get_json().get('coins', None)
        if coins==None:
            return "Record not found", 400
        
        amount = coins * ppc
        inApp = coins
    
    r = requests.post(URL_PAY_TOKEN, 
                    data={
                        'api': PAY_API,
                        'amount':amount,
                        'callback':str(url_for('user.verify', _external=True))
                    })
    
    token = r.json()['result']['token']
    url = r.json()['result']['url']

    pay = Payment(user_id=current_user.id, token=token, amount=amount, inApp=inApp)
    db.session.add(pay)
    db.session.commit()
    if request.method=="POST":
        return jsonify({'url':url})
    return redirect(url)

#verify handler
@app.route("/verify", methods=["GET"])
def verify():
    token = request.args.get('token')
    pay = Payment.query.filter(Payment.token==token).first_or_404()
    r = requests.post(URL_PAY_VERIFY, 
                    data={
                        'api': PAY_API,
                        'amount':pay.amount,
                        'token':token
                    })
    status = bool(r.json()['success'])
    if status:
        flash("payment_success")

        pay.status = "success"
        pay.card_pan = r.json()['result']['card_pan']
        pay.date = r.json()['result']['date']
        pay.refid = r.json()['result']['refid']
        pay.transaction_id = r.json()['result']['transaction_id']
        if pay.inApp==0:
            pay.user.pay = 1
            pay.user.coins = pay.user.coins + coin_04
        else:
            pay.user.coins = pay.user.coins + pay.inApp
        db.session.commit()
    else:
        flash("payment_failed")

        pay.status = "failed"
        pay.error = r.json()['error'][0]
        db.session.commit()
    return redirect(url_for("user.dashboard"))