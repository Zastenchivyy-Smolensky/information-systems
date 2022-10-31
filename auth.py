from flask import *
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,logout_user
from app import User, db
from werkzeug.security import generate_password_hash,check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("ログインが失敗しました")
            return redirect(url_for("auth.login"))
        login_user(user, remember=remember)
        flash("ログイン完了しました")
        return redirect(url_for("profile", user_id=user.id))

@auth.route("/signup" ,methods=["GET","POST"])
def signup():
    if request.method=="GET":
        return render_template("auth/signup.html")
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first() 
        if user:
            flash("")
            return redirect(url_for("auth.signup"))
            
        
        new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
        
@auth.route("/logout")
def logout():
    flash("ログアウトしました")
    logout_user()
    return redirect(url_for("index"))