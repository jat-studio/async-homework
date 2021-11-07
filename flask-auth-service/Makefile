export DBNAME=oauth_service
export DBUSER=oauth_service
export DBPASSWORD=oauth_service
export AUTHSECRET=secret
export EXPIRESSECONDS=3000

venv_create:
	python3.8 -m venv venv
	chmod +x venv/bin/activate

venv_activate: venv_create
	venv/bin/activate
	pip install -r requirements.txt

run: venv_activate
	python auth.py

get_token:
	curl -X POST -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1:8000/oauth/token/" -d "client_id=DXwNp4XRXzRA3BbuiQCCrAglDhMv5QQEgnDB3XWY" -d "client_secret=8L17rmX891KEAzAosWKUIEOwv4EZe9Xq3aElTfWPipeUSXAz4ESoFE4Xzd46zYumcPZ6QOh8WfWZVBANGb8wZAR8Krpo0JCOp3CQ0jgm2AEoDqmCdyUvSheAOcWOrImj" -d "code=GU1KvlZc2JIZb9Q0svBPLd4QDr7TDM" -d "redirect_uri=http://127.0.0.1:8000/oauth/callback" -d "grant_type=authorization_code"
