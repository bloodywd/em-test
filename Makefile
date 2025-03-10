# Makefile
MANAGE := uv run python3 manage.py

install:
	uv install

dev:
	@$(MANAGE) runserver

lint:
	poetry run flake8 task_manager --exclude=migrations

migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

test:
	@$(MANAGE) test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

shell:
	@$(MANAGE) shell_plus

start:
	uv run gunicorn -w 4 em_project.wsgi

build: install migrate