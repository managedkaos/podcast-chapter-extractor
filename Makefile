APP = $(notdir $(CURDIR))
TAG = $(shell echo "$$(date +%F)-$$(git rev-parse --short HEAD)")
DOCKER_REPO = ghcr.io/managedkaos


help:
	@echo "Run make <target> where target is one of the following..."
	@echo
	@echo "  all                      - run requirements, lint, test, and build"
	@echo "  requirements             - install runtime dependencies"
	@echo "  development-requirements - install development dependencies"
	@echo "  lint                     - run flake8, pylint, black, and isort checks"
	@echo "  black                    - format code with black"
	@echo "  isort                    - sort imports with isort"
	@echo "  test                     - run unit tests"
	@echo "  build                    - build docker container"
	@echo "  test-container           - run the container with test_chapters.json"
	@echo "  clean                    - clean up workspace and containers"

all: requirements lint test build

development-requirements: requirements
	pip install --quiet --upgrade --requirement development-requirements.txt

requirements:
	pip install --upgrade pip
	pip install --quiet --upgrade --requirement requirements.txt

lint:
	flake8 --ignore=E501,E231 *.py tests/*.py
	pylint --errors-only --disable=C0301 *.py tests/*.py
	black --diff *.py tests/*.py
	isort --check-only --diff *.py tests/*.py

fmt: black isort

black:
	black *.py tests/*.py

isort:
	isort *.py tests/*.py

test:
	python -m unittest discover -s tests -v --failfast

build: lint test
	docker build --tag $(APP):$(TAG) .

test-container:
	@echo "# Running container with test_chapters.json..."
	@mkdir -p test_output
	@docker run --rm \
		-v $(CURDIR)/tests/test_chapters.json:/data/test_chapters.json \
		-v $(CURDIR)/test_output:/data/test_output \
		$(APP):$(TAG) /data/test_chapters.json --output /data/test_output/chapters.txt

clean:
	docker container stop $(APP) || true
	docker container rm $(APP) || true
	@rm -rf ./__pycache__ ./tests/__pycache__ ./test_output
	@rm -f .*~ *.pyc

.PHONY: help requirements lint black isort test build clean development-requirements test-container
