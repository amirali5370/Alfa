from flask import Blueprint, render_template

app = Blueprint("general" , __name__)

@app.errorhandler(404)
def page_not_found(e):
    return "404", 404