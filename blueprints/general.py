from flask import Blueprint, render_template

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404page.html")

# فقط عنوان خطا برای 429
@app.errorhandler(429)
def ratelimit_handler(e):
    return "Too Many Requests", 429