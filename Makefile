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

# test:
#	        poetry run pytest --cov=task_manager/tests -vv --cov-report xml

.PHONY: install test lint check build
