from flask import Blueprint, redirect, render_template, url_for
import redis

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404page.html")

# فقط عنوان خطا برای 429
@app.errorhandler(429)
def ratelimit_handler(e):
    return "Too Many Requests", 429

@app.errorhandler(Exception)
def handle_error(e):
    if isinstance(e, redis.exceptions.ConnectionError):
        return redirect(url_for("home"))
    return redirect(url_for("home"))