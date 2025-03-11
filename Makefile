# Makefile
MANAGE := uv run python3 manage.py

install:
	uv pip install -r pyproject.toml

dev:
	@$(MANAGE) runserver

lint:
	uv run flake8 em_project --exclude=migrations

migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

test:
	@$(MANAGE) test

build: install migrate

start:
	uv run gunicorn -w 4 em_project.wsgi

build-no-uv:
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate

start-no-uv:
	gunicorn -w 4 em_project.wsgi