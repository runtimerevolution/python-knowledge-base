include .env
export

start:
	docker compose up -d

stop:
	docker compose down

migrate:
	python manage.py migrate --database default

runserver:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell

lint:
	poetry run flake8 .

black:
	 poetry run black .

makemigrate:
	python manage.py makemigrations

showmigrations:
	python manage.py showmigrations

createuser:
	python manage.py createsuperuser --database default

test:
	python manage.py test

py_test:
	pytest

clean:
	find . -name '*.py[co]' -delete
	find . -name '__pycache__'  -exec rm -r '{}' \;
	find . -name '.pytest_cache'  -exec rm -r '{}' \;
