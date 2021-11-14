import json
import random
import os
import uuid

from flask import Flask, redirect, render_template, request

import task_tracker_model
from rabbitmq_gateway import RabbitMQGateway


app = Flask(__name__)
rmq = RabbitMQGateway()


@app.route("/")
def main():
    user = task_tracker_model.verify(request.args.get("token"))

    if user:
        tasks = []
        if user["role"] in {"administrator", "manager"}:
            tasks = task_tracker_model.get_tasks()
        my_tasks = task_tracker_model.get_user_tasks(user_public_id=user["public_id"])
        return render_template("main.html", user=user, tasks=tasks, my_tasks=my_tasks)
    else:
        return redirect("http://localhost:5000/auth?service=task_tracker", code=302)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    user = task_tracker_model.verify(None)

    if user:
        if request.method == "GET":
            return render_template("add.html")
        else:
            task = task_tracker_model.add_task(
                public_id=str(uuid.uuid4()),
                description=request.form.get("description"),
                status="new",
                price=str(random.randint(1, 1000)),
                assign_to_public_id=None,
            )

            rmq.produce_cud_event(
                json.dumps(
                    {
                        "producer": "task_tracker",
                        "event_version": 1,
                        "event_name": "TaskCreated",
                        "data": {
                            "public_id": task["public_id"],
                            "description": task["description"],
                            "status": task["status"],
                            "price": task["price"],
                            "assign_to_public_id": task["assign_to_public_id"]
                        }
                    }
                )
            )

            return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=task_tracker", code=302)


@app.route("/complete")
def complete_task():
    user = task_tracker_model.verify(request.args.get("token"))

    if user:
        task = task_tracker_model.complete_task(public_id=request.args.get("public_id"))

        rmq.produce_cud_event(
            json.dumps(
                {
                    "producer": "task_tracker",
                    "event_version": 1,
                    "event_name": "TaskStatusChanged",
                    "data": {"public_id": task["public_id"], "status": task["status"]},
                }
            )
        )

        return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=task_tracker", code=302)


@app.route("/reassign")
def reassign_tasks():
    user = task_tracker_model.verify(request.args.get("token"))

    if user and user["role"] in {"administrator", "manager"}:
        users = task_tracker_model.get_users()
        new_tasks = task_tracker_model.get_tasks(only_new=True)

        for task in new_tasks:
            user = random.choice(users)
            task_tracker_model.assign_task(
                task_public_id=task["public_id"], user_public_id=user["public_id"]
            )

            rmq.produce_cud_event(
                json.dumps(
                    {
                        "producer": "task_tracker",
                        "event_version": 1,
                        "event_name": "TaskAssigned",
                        "data": {"public_id": task["public_id"], "assign_to_public_id": user["public_id"]},
                    }
                )
            )

        return {"success": True}
    else:
        return redirect("http://localhost:5000/auth?service=task_tracker", code=302)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5001)
