import os

from flask import Flask
from flask import render_template

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def info():
    return render_template("info.html")

@app.route("/family")
def family():
    return render_template("family.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/profile")
def profile():
    liff_id = os.getenv("LIFF_ID")
    return render_template("profile.html", liff_id=liff_id)


app.run(debug=True,host="0.0.0.0", port=5001)