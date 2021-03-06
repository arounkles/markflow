all: audits tests

# --- ENVIRONMENT MANAGEMENT ---
.PHONY: clean

clean:
	git clean -fdX
	# poetry returns a non-zero exit status if the virtualenv doesn't exist so we ignore
	# errors.
	-poetry env remove 3.6
	-poetry env remove 3.7
	-poetry env remove 3.8


.PHONY: clean _venv _venv_3.6 _venv_3.7 _venv_3.8 venvs
venvs: _venv_3.6 _venv_3.7 _venv_3.8

_venv:
	poetry env use ${PYTHON_VERSION}
	poetry install

_venv_3.6:
	PYTHON_VERSION=3.6 $(MAKE) _venv

_venv_3.7:
	PYTHON_VERSION=3.7 $(MAKE) _venv

_venv_3.8:
	PYTHON_VERSION=3.8 $(MAKE) _venv


# --- AUDITS ---
.PHONY: audits black flake8 markflow

# Runs all of our audits regardless of if any fail
audits:
	@status=0; \
	for target in black flake8 markflow; do \
		$(MAKE) $${target}; \
		status=$$(($$status + $$?)); \
		echo ""; \
	done; \
	exit $$status

black: _venv_3.8
	git ls-files | egrep '.*\.pyi?$$' | xargs poetry run black --check

flake8: _venv_3.8
	git ls-files | egrep '.*\.py$$' | egrep -v 'docs/' | \
		xargs poetry run flake8 --max-line-length 88

markflow: _venv_3.8
	git ls-files | egrep ".md$$" | grep -v "/files/" | poetry run markflow --check

# --- TESTS ---
.PHONY: tests
tests: utests mypy ensure_deps

ensure_deps:
	# Ensure dependencies markflow needs didn't sneak into dev dependencies
	poetry env use 3.8
	poetry install --no-dev
	poetry run markflow
	poetry install

# MyPy
.PHONY: mypy mypy_lib mypy_tests
mypy: mypy_lib mypy_tests

mypy_lib: _venv_3.8
	# --implicity-reexport means that we don't have to explicitly tell mypy about our
	# modules' members via a `__all__`
	MYPYPATH=$(CURDIR)/stubs poetry run mypy --strict --implicit-reexport markflow

mypy_tests: _venv_3.8
	# --implicity-reexport means that we don't have to explicitly tell mypy about our
	# modules' members via a `__all__`
	MYPYPATH=$(CURDIR)/stubs poetry run mypy --strict --implicit-reexport tests

# Unit Tests
# Bit of  a misnomer since `test_files.py` is more of a system/integration test
.PHONY: utests _utests utests_3.6 utests_3.7 utests_3.8
utests: utests_3.6 utests_3.7 utests_3.8

_utests:
	poetry env use ${PYTHON_VERSION}
	cd $(CURDIR)/tests && poetry run pytest --cov=markflow --cov-report=term \
		--cov-report=html --junit-xml=junit.xml
	@echo For more detailed information, see $(CURDIR)/tests/htmlcov/index.html

utests_3.6: _venv_3.6
	PYTHON_VERSION=3.6 $(MAKE) _utests

utests_3.7: _venv_3.7
	PYTHON_VERSION=3.7 $(MAKE) _utests

utests_3.8: _venv_3.8
	PYTHON_VERSION=3.8 $(MAKE) _utests

# --- EXPORTING ---
.PHONY: package

package:
	poetry build

# --- CI CONTAINER ---
.PHONY: container

container:
	docker build . -t markflow_builder
