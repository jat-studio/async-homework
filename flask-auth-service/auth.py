from flask import Flask, render_template, request
import json
import hashlib

import auth_model

# instantiate the Flask app.
app = Flask(__name__)


@app.route('/')
def list_clients():
    clients = auth_model.get_clients()
    return render_template('clients.html', clients=clients)


@app.route('/delete')
def delete_client():
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


@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("token")
    status = auth_model.blacklist(token)
    return {'success': status}


@app.route("/client", methods=["POST"])
def client() -> dict:
    if request.method == 'POST':
        uuid = request.form.get("uuid")
        email = request.form.get("email")
        full_name = request.form.get("full_name")
        position = request.form.get("position")
        is_active = request.form.get("is_active")
        role = request.form.get("role")

        # the client secret in the database is "hashed" with a one-way hash
        client_secret_input = request.form.get("client_secret")
        hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
        hashed_client_secret = hash_object.hexdigest()

        # make a call to the model to authenticate
        create_response = auth_model.create(
            hashed_client_secret=hashed_client_secret,
            uuid=uuid,
            email=email,
            full_name=full_name,
            position=position,
            is_active=is_active,
            role=role,
        )
        return {'success': create_response}
    else:
        return {'success': False}


# run the flask app.
if __name__ == "__main__":
    app.run(debug=True)
