from flask import Blueprint, jsonify, render_template, request, send_file, session, redirect, abort, flash, url_for
from config import ADMIN_PASSWORD, ADMIN_USERNAME

app = Blueprint("admin" , __name__)

@app.before_request
def before_request():
    if session.get("admin_login", None) == None and request.endpoint != "admin.login":
        abort(404)


# @app.route("/admin/login", methods = ["POST","GET"])
# def login():
#     if request.method == "POST":
#         username = request.form.get('username',None)
#         password = request.form.get('password',None)

#         if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#             session["admin_login"] = username

#             return "login"
#         else:
#             return "error"
#     else:
#         return "login page"
