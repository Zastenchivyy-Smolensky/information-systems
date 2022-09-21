from crypt import methods
from wsgiref.handlers import read_environ
from flask import *
from flask_fontawesome import FontAwesome
app = Flask(__name__)
import os
import secrets
from PIL import Image
from flask_sqlalchemy import SQLAlchemy

app.config["SECRET_KEY"]=secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///review.db'
db = SQLAlchemy(app)

UPLOAD_FOLDER = "./static/up"
ALLOWED_EXTENSIONS = set(['.png', '.jpg',".jpeg"])

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)#教科名
    teacher = db.Column(db.String(50), nullable=False)#教員名
    day = db.Column(db.String(50), nullable=False)#曜日
    time = db.Column(db.Integer, nullable=False)#開講時間
    review = db.Column(db.Integer, nullable=False)#開講時間
    point = db.Column(db.Integer, nullable=True)# 五段階評価
    pastImage = db.Column(db.String(100), nullable=False)#過去問ファイル
        


@app.route("/",methods=["GET","POST"])
def index():
    reviews = Review.query.all()

    data = ["kageyama","ryouta","kageyama"]
    return render_template("base.html", reviews=reviews)

@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        form_subject = request.form.get("subject")
        form_teacher = request.form.get("teacher")
        form_day = request.form.get("day")
        form_time = request.form.get("time")
        form_reivew=request.form.get("review")
        form_point = request.form.get("point")
        form_pastImage=request.files["pastImage"]
        _, ext = os.path.splitext(form_pastImage.filename)
        ext = ext.lower()
        if ext and ext in ALLOWED_EXTENSIONS:
            new_image = secrets.token_urlsafe(16) + ext.lower()
            i = Image.open(form_pastImage)
            i.thumbnail((200, 200))
            i.save(os.path.join(UPLOAD_FOLDER, new_image))
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
        return redirect(url_for("index"))
@app.route("/show/<int:id>")
def show(id):
    review = Review.query.get(id)
    return render_template("app/show.html", review=review)

@app.route("/edit/<int:id>" ,methods=["GET","POST"])
def edit(id):
    review = Review.query.get(id)
    return render_template("app/edit.html", review=review)

@app.route("/update/<int:id>/", methods=["POST"])
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

