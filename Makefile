# Makefile
MANAGE := uv run python3 manage.py

install:
	uv install

dev:
	@$(MANAGE) runserver

lint:
	uv run flake8 task_manager --exclude=migrations

migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

test:
	@$(MANAGE) test

test-coverage:
	uv run coverage run manage.py test
	uv run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	uv run coverage xml --include=task_manager/* --omit=task_manager/settings.py

shell:
	@$(MANAGE) shell_plus

start:
	gunicorn -w 4 em_project.wsgi

build:
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate