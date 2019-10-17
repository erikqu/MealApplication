from flask import Flask, render_template, url_for, request

app = Flask(__name__)


def check_database(username, password):
    # this function should check either a json
    # doc or check an actual DB (more work)
    return True


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        success = check_database(username, password)
        if not success:
            return render_template("login.html")
        else:
            return render_template("main.html")


@app.route("/home")
def main():
    return render_template("main.html")
