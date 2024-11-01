import os
import uuid
from datetime import datetime

from info import scrape_iwate_bousai
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

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
from database import FamilyInvitation
from init_data import init_shelter_data

load_dotenv()

app = Flask(__name__)

if os.getenv("DB_INIT") == "init":
    tables = [User, Family, Shelter, Hospital, Pharmacy, ReliefSuppliesCategory, ReliefSupplies, UserPosition, FamilyInvitation]
    db.drop_tables(tables)
    db.create_tables(tables)
    init_shelter_data()

app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def info():
    # line_id = session.get('line_id')
    # user = None
    # if line_id:
    #     user = User.select().where(User.line_id == line_id).first()
    # if not user:
    #     return redirect(url_for('profile'))
    iwate_bousai = scrape_iwate_bousai()
    return render_template("info.html",iwate_bousai=iwate_bousai)

@app.route("/family")
def family():
    # line_id = session.get('line_id')
    user = None
    # if line_id:
    #     user = User.select().where(User.line_id == line_id).first()
    # if not user:
    #     return redirect(url_for('profile'))
    # families = Family.select().where(Family.from_user == user.id)
    families = Family.select().where(Family.from_user == 1)
    family_invitation = FamilyInvitation.select().where(FamilyInvitation.invite_user == 1).first()
    if not family_invitation:
        FamilyInvitation.create(invite_user=1, code=uuid.uuid4(), created_at=datetime.now())
        db.commit()
        family_invitation = FamilyInvitation.select().where(FamilyInvitation.invite_user == 1).first()
    return render_template("family.html", user=user, families=families, family_invitation=family_invitation)

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
    line_id = session.get('line_id')
    user = None
    if line_id:
        user = User.select().where(User.line_id == line_id).first()
    if not user:
        return redirect(url_for('profile'))
    return render_template("map.html")

@app.route("/profile")
def profile():
    liff_id = os.getenv("LIFF_ID")
    line_id = session.get('line_id')
    user = None
    if line_id:
        user = User.select().where(User.line_id == line_id).first()
    return render_template("profile.html", liff_id=liff_id, user=user)

@app.route("/profile/save", methods=['POST'])
def profile_save():
    print(request.form['lineId'])
    print(request.form['address'])
    print(request.form['birthday'])
    print(request.form['gender'])
    session['line_id'] = request.form['lineId']
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
