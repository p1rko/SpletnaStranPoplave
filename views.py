from flask import Blueprint, render_template

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/vizija")
def vizija():
    return render_template("vizija.html")

@views.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

@views.route("/model")
def model():
    return render_template("model.html")