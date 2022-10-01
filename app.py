from flask import *
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,login_required, current_user
from werkzeug.security import generate_password_hash
import os
import secrets
app.config["SECRET_KEY"]=secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///review.db'
app.config["SECRET_KEY"]=os.urandom(24)

db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view="auth.login"
login_manager.init_app(app)
UPLOAD_FOLDER = "./static/up"
ALLOWED_EXTENSIONS = set(['.png', '.jpg',".jpeg"])

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)#教科名
    teacher = db.Column(db.String(50), nullable=False)#教員名
    day = db.Column(db.String(50), nullable=False)#曜日
    time = db.Column(db.Integer, nullable=False)#開講時間
    review = db.Column(db.Integer, nullable=False)#レビュー
    point = db.Column(db.Integer, nullable=True)# 五段階評価
    pastImage = db.Column(db.String(100), nullable=False)#過去問ファイル

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    userimage = db.Column(db.String(100))
    comment = db.Column(db.String(1000))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/",methods=["GET","POST"])
def index():

    reviews = Review.query.all()
    return render_template("base.html", reviews=reviews)

@app.route("/add", methods=["POST"])
@login_required
def add():
    if request.method == "POST":
        form_subject = request.form.get("subject")
        form_teacher = request.form.get("teacher")
        form_day = request.form.get("day")
        form_time = request.form.get("time")
        form_reivew=request.form.get("review")
        form_point = request.form.get("point")
        form_pastImage=request.files["pastImage"]
        form_pastImage.save(os.path.join("./static/up/",form_pastImage.filename))
        new_image = form_pastImage.filename
        review = Review(
            subject = form_subject,
            teacher = form_teacher,
            day = form_day,
            time = form_time,
            review = form_reivew,
            point = form_point,
            pastImage = new_image
        )
        db.session.add(review)
        db.session.commit()
        flash("投稿しました")
        return redirect(url_for("index"))

@app.route("/show/<int:id>")
def show(id):
    review = Review.query.get(id)
    return render_template("app/show.html", review=review)

@app.route("/edit/<int:id>" ,methods=["GET","POST"])
@login_required
def edit(id):
    review = Review.query.get(id)
    return render_template("app/edit.html", review=review)


@app.route("/update/<int:id>/", methods=["POST"])
@login_required
def update(id):
    review = Review.query.get(id)
    review.subject = request.form.get("subject")
    review.teacher = request.form.get("teacher")
    review.day = request.form.get("day")
    review.time = request.form.get("time")
    review.reivew=request.form.get("review")
    review.point = request.form.get("point")
    review.pastImage=request.files["pastImage"]
    review.pastImage.save(os.path.join("./static/up/",review.pastImage.filename))
    review.pastImage = review.pastImage.filename
    db.session.merge(review)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/review/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/search",methods=["POST"])
def search():
    item = request.form["item"]
    items = [("キャベツ",200),("にんじん",100),("牛乳",178),("もやし",50)]
    price="未登録"
    for row in items:
        if row[0] == item:
            price = str(row[1])+"円"
    return_json={
        "message":'<p>「{0}」は{1}です。</p>'.format(item, price)
    }
    return jsonify(values=json.dumps(return_json))

from .auth import auth
app.register_blueprint(auth)

@app.route("/profile")
@login_required
def profile():
    user=current_user
    return render_template("app/profile.html", user=user)

@app.route("/profile/edit/<int:user_id>")
def profile_edit(user_id):
    user = User.query.get(user_id)
    return render_template("app/profile_edit.html", user=user)


@app.route("/profile/update/<int:user_id>", methods=["POST"])
def profile_update(user_id):
    user = User.query.get(user_id)
    user.name = request.form.get("name")
    user.email = request.form.get("email")
    user.password = request.form.get("password")
    user.userimage=request.files["userimage"]
    user.comment = request.form.get("comment")
    user.password=generate_password_hash(user.password, method="sha256")
    user.userimage.save(os.path.join("./static/user/",user.userimage.filename))
    user.userimage = user.userimage.filename
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for("profile"))
