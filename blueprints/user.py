from flask import Blueprint, abort, render_template, request, redirect, send_file, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from flask_limiter import Limiter
from extentions import db, cache, limiter
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy import literal
from PIL import Image
import random
from functions.code_generators import invite_generator, auth_generator
from config import STATIC_SAVE_PATH
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


app = Blueprint("user" , __name__)

# limiter = Limiter()  # به app اصلی وصل خواهد شد
# limiter.limit("100 per minute")(app) 

# ------------- LOGIN AND REGISTER-------------
#register page
@app.route("/register", methods = ["POST","GET"],  strict_slashes=False)
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
            db.session.rollback()
            flash("unique")
            return redirect(request.url)

        if inviter != None:
            inv = Invite(inviter_id=inviter.id , invitee_id=user.id , assistant=assistant)
            inviter.coins += coin_02
            db.session.add(inv)
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
        return render_template("user/register.html", inviting=inviting, current_user=current_user, next=next)
    

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
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('user.home'))


@app.route("/",  strict_slashes=False)
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
    return render_template("user/guide.html", current_user=current_user)

@app.route("/support", methods = ["POST","GET"],  strict_slashes=False)
def support():
    if request.method == "POST":
        name = request.form.get('name',None)
        code = request.form.get('code',None)
        phone = request.form.get('phone',None)
        message = request.form.get('message',None)
        try:
            tick = Ticket(name=name, code=code, phone=phone, message=message)
            db.session.add(tick)
            db.session.commit()
            flash("ticket_add_success")
        except:
            db.session.rollback()
            flash("ticket_add_error")

        return redirect(request.url)
    else:
        return render_template("user/support.html", current_user=current_user)





#dashboard
@app.route("/dashboard", methods = ["POST","GET"],  strict_slashes=False)
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
            12: "دوازدهم"
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
@login_required
def account():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
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
        return render_template("user/account.html", current_user=current_user)
    

@app.route("/workbook",  strict_slashes=False)
@login_required
def workbook():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    workbooks = Workbook.query.filter(Workbook.user_id==current_user.id).order_by(Workbook.id.desc()).all()
    return render_template("user/workbook.html", current_user=current_user, workbooks=workbooks)

#books' file
@app.route('/download/workbook/<workbook_auth>')
@login_required
def single_workbook(workbook_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return abort(404)
    Workbook.query.filter(Workbook.auth==workbook_auth, Workbook.user_id==current_user.id).first()
    path = f"{STATIC_SAVE_PATH}/files/workbooks/{workbook_auth}.pdf"
    try:
        return send_file(path, as_attachment=True)
    except:
        return abort(404)
    

@app.route("/event",  strict_slashes=False)
@login_required
def event():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    events = News.query.filter((News.grade_bits.op('&')(literal(current_user.period_code))) != 0).order_by(News.id.desc()).all()
    return render_template("user/event.html", current_user=current_user, events=events)


@app.route("/pamphlet",  strict_slashes=False)
@login_required
def pamphlet():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    pamphlets = Pamphlet.query.filter((Pamphlet.grade_bits.op('&')(literal(current_user.period_code))) != 0).order_by(Pamphlet.id.desc()).all()
    return render_template("user/pamphlet.html", current_user=current_user, pamphlets=pamphlets)

#books' file
@app.route('/download/pamphlet/<pamphlet_auth>')
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
    


@app.route("/quiz",  strict_slashes=False)
@login_required
def quiz():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    items = Quiz.query.filter((Quiz.grade_bits.op('&')(literal(current_user.period_code))) != 0).order_by(Quiz.start_time).all()
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
@login_required
def single_quiz(quiz_auth):
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    
    quiz = Quiz.query.filter_by(auth=quiz_auth).first_or_404()
    r = Result.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).first()
    if request.method == "POST":
        true = 0
        questions = {q.id: q for q in quiz.questions}
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

        questions = random.sample(quiz.questions.all(), quiz.count)
        return render_template("user/single_quiz.html", quiz=quiz, questions=questions)


@app.route("/api/result", methods = ["POST","GET"], strict_slashes=False)
@login_required
def result():
    if current_user.completion == 0 or current_user.pay == 0:
        return abort(404)
    print(request)
    data = request.get_json()
    quiz_id = int(data.get('quiz_id',None))

    r = Result.query.filter(Result.user_id==current_user.id, Result.quiz_id==quiz_id).first_or_404()

    return jsonify({'result': r.score})



@app.route("/webinar",  strict_slashes=False)
@login_required
def webinar():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    items = Webinar.query.filter((Webinar.grade_bits.op('&')(literal(current_user.period_code))) != 0).order_by(Webinar.start_time).all()
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


@app.route("/course",  strict_slashes=False)
@login_required
def course():
    if current_user.completion == 0 or current_user.pay == 0:
        return redirect(url_for("user.dashboard"))
    courses = Course.query.filter((Course.grade_bits.op('&')(literal(current_user.period_code))) != 0).order_by(Course.id.desc()).all()

    return render_template("user/course.html", courses=courses)