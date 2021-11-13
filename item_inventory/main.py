import os
import uuid
from flask import Flask, redirect, render_template, request

import inventory_model

app = Flask(__name__)


@app.route("/")
def main():
    user = inventory_model.verify(request.args.get("token"))

    if user:
        items = inventory_model.get_items(user=user, w_all=user["role"] == "administrator")
        return render_template("main.html", user=user, items=items)
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    user = inventory_model.verify(None)

    if user:
        if request.method == "GET":
            return render_template("add.html")
        else:
            inventory_model.add_item(
                public_id=str(uuid.uuid4()),
                title=request.form.get("title"),
                description=request.form.get("description"),
                status=request.form.get("status"),
            )
            return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5001)
