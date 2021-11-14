import os
from flask import Flask, redirect, render_template, request

import fix_cms_model
from rabbitmq_gateway import RabbitMQGateway


app = Flask(__name__)
rmq = RabbitMQGateway()


@app.route("/")
def main():
    user = fix_cms_model.verify(request.args.get("token"))

    if user and user["role"] in ("administrator", "repairman"):
        items = fix_cms_model.get_items()
        return render_template("main.html", user=user, items=items)
    else:
        return redirect("http://localhost:5000/auth?service=fix_cms", code=302)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5002)
