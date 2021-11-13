import uuid
from flask import Flask, g, render_template, request
import json
import hashlib

import auth_model

from rabbitmq_gateway import RabbitMQGateway

app = Flask(__name__)
rmq = RabbitMQGateway()


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/create', methods=['POST'])
def add_user():
    hash_object = hashlib.sha1(bytes(request.form.get('password'), 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    user = auth_model.create(
        hashed_client_secret=hashed_client_secret,
        public_id=str(uuid.uuid4()),
        email=request.form.get('email'),
        full_name=request.form.get('full_name'),
        position="position",
        is_active=True,
        role="employee",
    )

    rmq.produce_cud_event(
        json.dumps(
            {
                "producer": "oauth",
                "event_version": 1,
                "event_name": "AccountCreated",
                "data": {
                    "public_id": user["public_id"],
                    "email": user["email"],
                    "full_name": user["full_name"],
                    "role": user["role"],
                }
            }
        )
    )

    return {'success': True}


@app.route('/')
def list_users():
    users = auth_model.get_users()
    return render_template('users.html', users=users)


@app.route('/delete')
def delete_user():
    public_id = request.args.get("public_id")
    auth_model.delete(public_id)

    rmq.produce_cud_event(
        json.dumps(
            {
                "producer": "oauth",
                "event_version": 1,
                "event_name": "AccountDeleted",
                "data": {"public_id": public_id},
            }
        )
    )

    return {'success': True}


# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        return render_template('auth.html')
    else:
        # get the client_id and secret from the client application
        email = request.form.get("email")
        client_secret_input = request.form.get("client_secret")

        # the client secret in the database is "hashed" with a one-way hash
        hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
        hashed_client_secret = hash_object.hexdigest()

        # make a call to the model to authenticate
        authentication = auth_model.authenticate(email, hashed_client_secret)
        return {'success': False} if not authentication else json.dumps(authentication)


# API route for verifying the token passed by API calls
@app.route("/verify", methods=["POST"])
def verify():
    # verify the token 
    authorization_header = request.headers.get('authorization')
    token = authorization_header.replace("Bearer ", "")
    verification = auth_model.verify(token)

    return verification


@app.route("/edit")
def edit_user():
    return render_template('edit.html', user=auth_model.get_user(public_id=request.args.get("public_id")))


@app.route("/update", methods=["POST"])
def update_user():
    user, is_role_changed = auth_model.update_user(
        public_id=request.form.get("public_id"),
        email=request.form.get('email'),
        full_name=request.form.get('full_name'),
        position=request.form.get('position'),
        is_active=True if request.form.get('is_active') == 'True' else False,
        role=request.form.get('role'),
    )

    if is_role_changed:
        rmq.produce_business_event(
            json.dumps(
                {
                    "producer": "oauth",
                    "event_version": 1,
                    "event_name": "AccountRoleChanged",
                    "data": {"public_id": user["public_id"], "role": user["role"]},
                }
            )
        )
    else:
        rmq.produce_cud_event(
            json.dumps(
                {
                    "producer": "oauth",
                    "event_version": 1,
                    "event_name": "AccountUpdated",
                    "data": {
                        "public_id": user["public_id"],
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "role": user["role"],
                    }
                }
            )
        )

    return {'success': True}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# run the flask app.
if __name__ == "__main__":
    app.run(debug=True)
