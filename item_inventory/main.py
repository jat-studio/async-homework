import json
import os
import uuid
from flask import Flask, redirect, render_template, request

import inventory_model
from rabbitmq_gateway import RabbitMQGateway


app = Flask(__name__)
rmq = RabbitMQGateway()


@app.route("/")
def main():
    user = inventory_model.verify(request.args.get("token"))

    if user:
        items = inventory_model.get_items(user=user, w_all=True) if user["role"] == "administrator" else []
        myitems = inventory_model.get_items(user=user, w_all=False)
        return render_template("main.html", user=user, items=items, myitems=myitems)
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


@app.route("/add", methods=["GET", "POST"])
def add_item():
    user = inventory_model.verify(None)

    if user:
        if request.method == "GET":
            return render_template("add.html")
        else:
            item = inventory_model.add_item(
                public_id=str(uuid.uuid4()),
                title=request.form.get("title"),
                description=request.form.get("description"),
                status=request.form.get("status"),
            )

            rmq.produce_cud_event(
                json.dumps(
                    {
                        "producer": "item_inventory",
                        "event_version": 1,
                        "event_name": "ItemCreated",
                        "data": {
                            "public_id": item["public_id"],
                            "title": item["title"],
                            "description": item["description"],
                            "status": item["status"],
                        }
                    }
                )
            )

            return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


@app.route("/book")
def book_item():
    user = inventory_model.verify(request.args.get("token"))

    if user:
        inventory_model.book_item(public_id=request.args.get("public_id"))
        return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


@app.route("/unbook")
def unbook_item():
    user = inventory_model.verify(request.args.get("token"))

    if user:
        inventory_model.unbook_item(public_id=request.args.get("public_id"))
        return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


@app.route("/broken")
def broken_item():
    user = inventory_model.verify(request.args.get("token"))

    if user:
        public_id = request.args.get("public_id")
        inventory_model.broken_item(public_id=public_id)

        rmq.produce_business_event(
            json.dumps(
                {
                    "producer": "item_inventory",
                    "event_version": 1,
                    "event_name": "ItemBroken",
                    "data": {
                        "public_id": public_id,
                        "requester_public_id": user["public_id"],
                    }
                }
            )
        )

        return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=item_inventory", code=302)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5001)
