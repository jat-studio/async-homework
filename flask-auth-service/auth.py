import uuid
from flask import Flask, g, render_template, request
import json
import hashlib

import auth_model

# instantiate the Flask app.
app = Flask(__name__)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/create', methods=['POST'])
def add_user():
    hash_object = hashlib.sha1(bytes(request.form.get('password'), 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    create_response = auth_model.create(
        hashed_client_secret=hashed_client_secret,
        uuid=str(uuid.uuid4()),
        email=request.form.get('email'),
        full_name=request.form.get('full_name'),
        position="position",
        is_active=True,
        role="employee",
    )

    return {'success': create_response}


@app.route('/')
def list_users():
    users = auth_model.get_users()
    return render_template('users.html', users=users)


@app.route('/delete')
def delete_user():
    auth_model.delete(request.args.get("uuid"))
    return {'success': True}


# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["POST"])
def auth():	
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
    return render_template('edit.html', user=auth_model.get_user(uuid=request.args.get("uuid")))


@app.route("/update", methods=["POST"])
def update_user():
    update_response = auth_model.update_user(
        email=request.form.get('email'),
        full_name=request.form.get('full_name'),
        position=request.form.get('position'),
        is_active=True if request.form.get('is_active') == 'True' else False,
        role=request.form.get('role'),
    )

    return {'success': update_response}


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# run the flask app.
if __name__ == "__main__":
    app.run(debug=True)
