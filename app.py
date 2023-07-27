from email.policy import default
from flask import *
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,login_required, current_user,login_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
import os
import secrets
from sqlalchemy import or_
import sqlite3 
import matplotlib
matplotlib.use('agg')




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
    good_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    good = False

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    userimage = db.Column(db.String(100))
    comment = db.Column(db.String(1000))
    reivews = db.relationship("Review", backref="user",
                            lazy="dynamic", cascade="delete")

class Good(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"))
    user = db.relationship('User', backref=db.backref('good', lazy=True))
    review = db.relationship('Review', backref=db.backref('good', lazy=True))
    



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/",methods=["GET","POST"])
def index():
    review_input = request.args.get("search")
    if review_input is None or len(review_input) == 0:
        reviews = Review.query.join(User).all()
    else: 
        reviews = db.session.query(Review).filter(or_(Review.subject.like(review_input), Review.teacher.like(review_input))).all()

    return render_template("base.html", reviews=reviews)

@app.route("/graph")
def chart_do():
    dbname = "review.db"
    connection = sqlite3.connect(dbname)
    cur = connection.cursor()
    sql1 = "SELECT teacher,point from review"
    result = cur.execute(sql1)
    graph_data=[{"x":row[0],"y":row[1]} for row in result]
    return jsonify(graph_data)
    # plt.plot(y_data)
    # plt.xlabel("X軸")
    # plt.ylabel("Y軸")
    # plt.title("graph")
    # plt.savefig("static/graph.png")
    # graph_image="static/graph.png"
    # return render_template("app/graph.html", graph_image=graph_image)


@app.route("/add", methods=["POST"])
@login_required
def add():
    if request.method == "POST":
        user = User.query.filter_by(id=current_user.id).all()[0]
        user.subject = request.form.get("subject")
        user.teacher = request.form.get("teacher")
        user.day = request.form.get("day")
        user.time = request.form.get("time")
        user.review=request.form.get("review")
        user.point = request.form.get("point")
        user.pastImage=request.files["pastImage"]
        user.pastImage.save(os.path.join("./static/up/",user.pastImage.filename))
        new_image = user.pastImage.filename
        review = Review(
            subject = user.subject,
            teacher = user.teacher,
            day = user.day,
            time = user.time,
            review = user.review,
            point = user.point,
            pastImage = new_image,
            user_id = user.id
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



@app.route("/login", methods=["GET","POST"])
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

@app.route("/signup" ,methods=["GET","POST"])
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
        
@app.route("/logout")
def logout():
    flash("ログアウトしました")
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
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
    return redirect(url_for("profile",user_id=user.id))



@app.route("/good", methods=["POST"])
def good():
    review_id = request.json["review_id"]
    review = Review.query.filter_by(id=review_id).all()[0]
    user_id = current_user.id
    good = Good.query.filter_by(review_id=review_id, user_id=user_id).all()
    if len(good)>=1:
        db.session.delete(good[0])
        review.good_count = review.good_count - 1
    else:
        good_user = Good(review_id=review_id, user_id=user_id)
        db.session.add(good_user)
        review.good_count = review.good_count+1
    db.session.commit()
    return str(review.good_count)
    