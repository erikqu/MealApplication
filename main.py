from flask import Flask, render_template, url_for, request
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
            return render_template("main.html", username)


@app.route("/Events")
def events():
    return render_template("events.html")


@app.route("/home")
def main(user : str):
    # get the user json and read in (this assumes we have a dictionary already)
    recipes = user["recipes"]

    return render_template("main.html", recipes)
