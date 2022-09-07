from unicodedata import name
from flask import *
from flask_fontawesome import FontAwesome
app = Flask(__name__)


@app.route("/")
def index():
    data = ["kageyama","ryouta","kageyama"]
    return render_template("index.html", data=data)


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

@app.route("/test")
def test():
    return render_template("index2.html")