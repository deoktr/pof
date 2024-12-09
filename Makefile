.PHONY: test coverage format lint build_docker


test:
	python3 -m pytest

coverage: test
	python3 -m coverage html

format:
	python3 -m black .
	python3 -m ruff format .

lint:
	python3 -m ruff check .

build_docker:
	docker build -t pof .
