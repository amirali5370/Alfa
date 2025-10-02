from flask import Blueprint, render_template, request, render_template_string
import redis

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404page.html")

# فقط عنوان خطا برای 429
@app.errorhandler(429)
def ratelimit_handler(e):
    return "Too Many Requests", 429

@app.errorhandler((redis.exceptions.TimeoutError))
def handle_redis_errors(e):
    # ارسال به صفحه خطا با مسیر فعلی
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Redis Error</title>
    <script>
        setTimeout(function() {
            window.location.href = '"""+str(request.url)+"""';
        }, 5000);
    </script>
</head>
<body>
    <h1>در تلاش برای اتصال</h1>
    <p>لطفا کمی صبر نمایید</b></p>
</body>
</html>
"""), 503
@app.errorhandler((redis.exceptions.ConnectionError))
def handle_redis_errors(e):
    # ارسال به صفحه خطا با مسیر فعلی
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Redis Error</title>
    <script>
        setTimeout(function() {
            window.location.href = '"""+str(request.url)+"""';
        }, 5000);
    </script>
</head>
<body>
    <h1>در تلاش برای اتصال</h1>
    <p>لطفا کمی صبر نمایید</b></p>
</body>
</html>
"""), 503