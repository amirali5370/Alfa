from flask import Blueprint, abort, render_template, request, redirect, send_file, url_for, flash, jsonify
from flask_login import login_user, login_required, current_user, logout_user

app = Blueprint("user" , __name__)

#login page
@app.route("/login", methods = ["POST","GET"],  strict_slashes=False)
def login():

    # login_user(user)

    return "login"