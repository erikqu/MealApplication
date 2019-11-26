from flask import Flask, render_template, url_for, request, json, redirect
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)


def add_user_to_database(username, password, filename="hashes.txt"):
    # add a check if the file exists or not
    passfile = open(filename, "r")
    data = eval(passfile.read())
    passfile.close()
    passfile = open(filename, "w")
    password_hash = generate_password_hash(password)
    data[username] = password_hash
    passfile.write(str(data))
    passfile.close()


def check_database(username, password):
    password_file = open("hashes.txt", 'r')
    password_file = password_file.read()
    data = eval(password_file)
    # iterate through all hashes and find that hash.
    for key in data:
        curhash = data[key]
        if key == username:
            if check_password_hash(curhash, password):
                return True
    return False


def open_json(filename):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", filename)
    return json.load(open(json_url))


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        success = check_database(username, password)
        if not success:
            return render_template("login.html", loginfail = True)
        else:
            user = open_json("fake_user.json")
            return redirect(url_for("main", user=user['username']))


@app.route("/cookbook/<user>")
def cookbook(user : str):
    user = open_json("fake_user.json")
    return render_template("cookbook.html", user=user['username'], recipes=user['cookbook_recipes'])


@app.route("/messages/<user>")
def messages(user : str):
    return render_template("messages.html", user=user)


@app.route("/events/<user>")
def events(user : str):
    return render_template("events.html", user=user)


@app.route("/settings/<user>")
def settings(user : str):
    return render_template("settings.html", user=user)


@app.route("/home/<user>")
def main(user : str):
    # get the user json and read in (this assumes we have a dictionary already)
    user = open_json("fake_user.json")
    return render_template("main.html", user=user['username'], recipes=user['timeline_recipes'],
                            latest_comment=user['latest_comment'], top_recipes=user['top_recipes'])
