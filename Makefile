install:
	        poetry install

check:
	        poetry check

build:
	        poetry build

publish:
	        poetry publish --dry-run

package-install:
	        pip install --user dist/*.whl

lint:
	        poetry run flake8 task_manager --exclude settings.py

shell:
		poetry run python manage.py shell

# test:
#	        poetry run pytest --cov=task_manager/tests -vv --cov-report xml

test:
		poetry run python manage.py test

server:
		poetry run python3 manage.py runserver


.PHONY: install test lint check build
