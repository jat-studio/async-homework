from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def main():
    return render_template("main.html", user=request.args.get("user"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
