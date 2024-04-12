FLASK_ENV ?= development

.PHONY: venv install db run test test-coverage lint lint-fix format

venv:
	python -m venv venv
	. venv/bin/activate

install:
	. venv/bin/activate && \
	pip install -r requirements.txt

db:
	. venv/bin/activate && \
	python manage.py db init && \
	python manage.py db migrate && \
	python manage.py db upgrade

run:
	. venv/bin/activate && \
	FLASK_ENV=$(FLASK_ENV) python manage.py run

test:
	. venv/bin/activate && \
	python manage.py test

test-coverage:
	. venv/bin/activate && \
	pytest --cov=app ./app/test

seed-db:
	@python -m app.common.scripts.seed_database       

clean-db:
	@python -m app.common.scripts.clean_database

lint:
	. venv/bin/activate && \
	ruff check *.py

lint-fix:
	. venv/bin/activate && \
	ruff check --fix *.py

format:
	. venv/bin/activate && \
	isort ./app
	ruff check --fix-only ./app
	black ./app