.PHONY: clean clean-test clean-pyc clean-build docs
.DEFAULT_GOAL := help

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -rf tests/testcontent/downloaded/*
	rm -rf tests/testcontent/generated/*

lint: ## check style with flake8
	flake8 src/treediffer tests

test: clean-test ## run tests quickly with the default Python
	pytest

test-all: clean-test ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	pip install coverage pytest
	coverage run --source src/treediffer -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docsclean:
	$(MAKE) -C docs clean
	rm -f docs/_build/*

docs: ## generate Sphinx HTML documentation
	pip install -r docs/requirements.txt
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	# $(BROWSER) docs/build/html/index.html

latexdocs:
	pip install -r docs/requirements.txt
	$(MAKE) -C docs clean
	$(MAKE) -C docs latex

release: clean ## package and upload a release
	pip install twine
	python setup.py sdist
	twine upload dist/*
