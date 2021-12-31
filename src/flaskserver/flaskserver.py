from flask import Flask, redirect, url_for, request, render_template

# https://testdriven.io/courses/learn-flask/
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}"


@app.route("/success/<string:name>")
def success(name):
    return f"Welcome {name}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("success", name=user))
    else:
        return render_template("demo.html", request="please")


if __name__ == "__main__":
    app.run(debug=True)
