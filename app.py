import os
from info import scrape_iwate_bousai
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from dotenv import load_dotenv

from database import db
from database import User
from database import Family
from database import Shelter
from database import Hospital
from database import Pharmacy
from database import ReliefSuppliesCategory
from database import ReliefSupplies
from database import UserPosition

from init_data import init_shelter_data

load_dotenv()

app = Flask(__name__)

if os.getenv("DB_INIT") == "init":
    tables = [User, Family, Shelter, Hospital, Pharmacy, ReliefSuppliesCategory, ReliefSupplies, UserPosition]
    db.drop_tables(tables)
    db.create_tables(tables)
    init_shelter_data()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def info():
    iwate_bousai = scrape_iwate_bousai()
    return render_template("info.html",iwate_bousai=iwate_bousai)

@app.route("/family/<id>")
def family(id):
    user = User.select().where(User.id == id).first()
    print(user)
    families = []
    if user:
        families = Family.select().where(Family.from_user == user.id)
    return render_template("family.html", families=families)

@app.route("/family/add", methods=['POST'])
def add_family():
    if request.method == 'POST':
        line_id = request.form['line_id']
        try:
            to_user = User.get(User.line_id == line_id)
            from_user = User.get(User.id == request.form['user_id'])
            Family.create(from_user=from_user, to_user=to_user)
            return redirect(url_for('family', id=from_user.id))
        except User.DoesNotExist:
            return redirect(url_for('family', id=request.form['user_id']))
    return redirect(url_for('family', id=request.form['user_id']))

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/profile")
def profile():
    liff_id = os.getenv("LIFF_ID")
    return render_template("profile.html",liff_id=liff_id)

@app.route("/profile/save", methods=['POST'])
def profile_save():
    line_id = request.form['lineId']
    name    = request.form["name"]
    address  = request.form['address']
    birthday = request.form['birthday']
    gender = request.form['gender']
    User.create(line_id = line_id,name=name,address=address,birthday=birthday,gender=gender)
    return redirect("/profile")

@app.route("/shelter/relief_supplies/login")
def relief_supplies_login():
    return render_template("shelter/relief_supplies/login.html")

@app.route("/shelter/relief_supplies/top")
def relief_supplies_top():
    return render_template("shelter/relief_supplies/top.html")

if os.getenv("ENV") == "development":
    app.run(host="0.0.0.0", port=5001, ssl_context=('ssl/cert.pem', 'ssl/private.key'),debug=True)
else:
    app.run(debug=True,host="0.0.0.0", port=5001)
