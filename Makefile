GLOBAL_PY := python3.8
BUILD_VENV ?= .venv
BUILD_PY := $(BUILD_VENV)/bin/python

.PHONY: init
init: $(BUILD_VENV)

$(BUILD_VENV):
	$(GLOBAL_PY) -m venv $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip
	$(BUILD_PY) -m pip install black
	$(BUILD_PY) -m pip install -r ./backend/requirements.txt


.PHONY: run
run:
	DOT_ENV_FILE=true \
	$(BUILD_VENV)/bin/python backend/manage.py runserver
