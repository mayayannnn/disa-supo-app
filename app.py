import os
import uuid
from datetime import datetime

from info import scrape_iwate_bousai,scrape_terebi_saigai
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
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
from init_data import *

from peewee import JOIN

load_dotenv()

app = Flask(__name__)

if os.getenv("DB_INIT") == "init":
    tables = [User, Family, Shelter, Hospital, Pharmacy, ReliefSuppliesCategory, ReliefSupplies, UserPosition, FamilyInvitation]
    db.drop_tables(tables)
    db.create_tables(tables)
    init_shelter_data()
    init_hospital_data()
    init_pharmacy_data()
    init_reliefsupplies_data()
    init_reliefsuppliescategory_date()


app.secret_key = os.urandom(24)
app.config["SESSION_COOKIE_HTTPONLY"] = True


@app.route("/")
def index():
    return redirect(url_for("info"))

@app.route("/detail/<id>")
def detail(id):
    shelter = Shelter.get(Shelter.id == id)
    reliefsupplies = ReliefSupplies.select(ReliefSupplies,ReliefSuppliesCategory).join(ReliefSuppliesCategory,on=ReliefSupplies.reliefsuppliescategory_id == ReliefSuppliesCategory.id).where(ReliefSupplies.shelter_id == id)
    return render_template("/detail.html",shelter=shelter,reliefsupplies=reliefsupplies)

@app.route("/info")
def info():
    line_id = session.get('line_id')
    user = None
    if line_id:
        user = User.select().where(User.line_id == line_id).first()
    if not user:
        return redirect(url_for('profile'))
    iwate_bousai = scrape_iwate_bousai()
    terebi = scrape_terebi_saigai()
    print(terebi)
    # x_tweets = search_disaster_tweets_v2("災害 OR 地震 OR 津波", count=10)
    return render_template("info.html",iwate_bousai=iwate_bousai,terebi=terebi)

@app.route("/family")
def family():
    #ユーザーポジションを登録
    line_id = session.get('line_id')
    user = None
    if line_id:
        user = User.select().where(User.line_id == line_id).first()
    if not user:
        return redirect(url_for('profile'))
    # families = (Family .select(Family, User, UserPosition).join(User, on=(Family.to_user_id == User.id))
    #             .join(UserPosition, on=(UserPosition.user == User.id)).where(Family.from_user == user.id))
    # サブクエリ1: 自分が招待した人
    subquery1 = (Family
                .select(Family.to_user_id.alias('id'))
                .where(Family.from_user_id == user.id))
    # サブクエリ2: 自分を招待してくれた人
    subquery2 = (Family
                .select(Family.from_user_id.alias('id'))
                .where(Family.to_user_id == user.id))
    # UNION ALL でサブクエリを結合
    union_subquery = subquery1.union_all(subquery2)
    # メインクエリ: User と UserPosition を結合
    families = (User
            .select()
            .where(User.id.in_(union_subquery)))
    for f in families:
        user_position = UserPosition.select().where(UserPosition.user == f.id).order_by(UserPosition.id.desc()).first()
        f.Latitude = user_position.Latitude
        f.Longitude = user_position.Longitude
    family_invitation = FamilyInvitation.select().where(FamilyInvitation.invite_user == user.id).first()
    if not family_invitation:
        FamilyInvitation.create(invite_user=user.id, code=uuid.uuid4(), created_at=datetime.now())
        db.commit()
        family_invitation = FamilyInvitation.select().where(FamilyInvitation.invite_user == 1).first()
    # 有効期限チェック - 作成から24時間経過している場合は再作成
    elif (datetime.now() - family_invitation.created_at).total_seconds() > 24 * 60 * 60:
        family_invitation.delete_instance()
        FamilyInvitation.create(invite_user=user.id, code=uuid.uuid4(), created_at=datetime.now())
        db.commit()
        family_invitation = FamilyInvitation.select().where(FamilyInvitation.invite_user == 1).first()
    return render_template("family.html", user=user, families=families, family_invitation=family_invitation)

@app.route("/family/del/<user_id>/<family_id>", methods=['POST'])
def family_dele(user_id,family_id):
    Family.delete().where(Family.from_user == user_id,Family.to_user == family_id).execute()
    Family.delete().where(Family.from_user == family_id,Family.to_user == user_id).execute()
    return redirect("/family")

@app.route("/invite/<code>")
def invite(code):
    line_id = session.get('line_id')
    print(line_id)
    family_invitation = FamilyInvitation.select().where(FamilyInvitation.code == code).first()
    # 有効期限チェック - 作成から24時間経過している場合は無効
    if family_invitation and (datetime.now() - family_invitation.created_at).total_seconds() < 24 * 60 * 60:
        # 招待した人のユーザー情報を取得
        invite_user = family_invitation.invite_user
        from_user = User.get(User.id == invite_user)        
        # 招待された人のユーザー情報を取得 (現在は仮のユーザーID=1を使用)
        to_user = User.select().where(User.line_id == line_id).first()
        # 家族として登録
        Family.create(from_user=from_user, to_user=to_user)
        return redirect("/family")
    else:
        return redirect("/invalid-invite")

@app.route("/invalid-invite")
def invalid_invite():
    return render_template("invalid_invite.html")

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
    shelters = Shelter.select()
    hospitals = Hospital.select()
    pharmacies = Pharmacy.select()
    return render_template(
        "map.html",
        shelters=shelters,
        hospitals=hospitals,
        pharmacies=pharmacies,
        user_id=user.id
    )

@app.route("/shelter_list")
def shelter_list():
    search = request.args.get("search")
    if search:
        # searchs = ReliefSuppliesCategory.select().where(ReliefSuppliesCategory.name.contains(search))
        relief_supplies = ReliefSupplies.select().join(ReliefSuppliesCategory).switch(ReliefSupplies).join(Shelter).where(
            Shelter.name.contains(search) | ReliefSuppliesCategory.name.contains(search)
        )
        return render_template("shelter_list.html", relief_supplies=relief_supplies)
    else:
        return render_template("shelter_list.html")


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
    liff_id = os.getenv("LIFF_ID")
    line_id = session.get('line_id')
    line_id = request.form['lineId']
    user = User.select().where(User.line_id == line_id).first()
    name    = request.form["name"]
    address  = request.form['address']
    birthday = request.form['birthday']
    gender = request.form['gender']
    if user == None:
        User.create(line_id = line_id,name=name,address=address,birthday=birthday,gender=gender)
        session['line_id'] = line_id
    else:
        user.line_id  = line_id
        user.name     = name
        user.address  = address
        user.birthday = birthday
        user.gender   = gender
        user.save()
        session['line_id'] = line_id
    return redirect("/profile")

@app.route("/shelter/relief_supplies/login")
def relief_supplies_login():
    return render_template("shelter/relief_supplies/login.html")

@app.route("/shelter/relief_supplies/top")
def relief_supplies_top():
    return render_template("shelter/relief_supplies/top.html")

@app.route("/qa")
def qa():
    return render_template("qa.html")

@app.route("/register_position", methods=['POST'])
def register_position():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    user_id = data['user_id']
    UserPosition.create(user_id=user_id, Latitude=latitude, Longitude=longitude)
    return jsonify({'status': 'success'})

if os.getenv("ENV") == "development":
    app.run(host="0.0.0.0", port=5001, ssl_context=('ssl/cert.pem', 'ssl/private.key'),debug=True)
else:
    app.run(debug=True,host="0.0.0.0", port=5001)
