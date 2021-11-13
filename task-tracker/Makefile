venv_create:
	python3.8 -m venv venv
	chmod +x venv/bin/activate

venv_activate: venv_create
	venv/bin/activate
	pip install -r requirements.txt

run: venv_activate
	python task_tracker.py

run_consumer: venv_activate
	python consumer.py
