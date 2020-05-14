.PHONY: all

all: clean lint test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf lint/
	rm -f .coverage
	rm -rf junit/
	rm -rf coverage-reports/
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint:
	pip install flake8 --upgrade
	mkdir -p lint
	flake8 . --exclude=.venv --count --exit-zero --max-complexity=10 --max-line-length=119 --statistics --output=lint/flake8.out --tee

test: 
	pip install pytest pytest-cov pytest-mock --upgrade
	pytest tests/ --cov=aws_sso --junitxml=junit/test-results.xml --cov-report=xml:coverage-reports/coverage.xml --cov-report=html:coverage-reports/html
