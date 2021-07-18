GLOBAL_PY := python3
BUILD_VENV ?= .venv
BUILD_PY := $(BUILD_VENV)/bin/python

.PHONY: init-backend
init-backend: $(BUILD_VENV)

$(BUILD_VENV):
	$(GLOBAL_PY) -m venv $(BUILD_VENV)
	$(BUILD_PY) -m pip install -U pip
	$(BUILD_PY) -m pip install black
	$(BUILD_PY) -m pip install -r ./backend/requirements.txt


.PHONY: run-backend
run-backend:
	DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
	DJANGO_DEBUG=true \
	DJANGO_MEDIA_PATH=./media/ \
	DJANGO_MEDIA_URL=/media/ \
	DJANGO_SECRET_KEY="(xjy7s2tt$z4mt^4ye_=ru2_yfb=e%&@mn=ldmkp38ztq4rjiy" \
	DJANGO_SQLITE_DB_FILE=./data/db.sqlite3 \
	DJANGO_STATIC_ROOT=/app/dist/assets/ \
	DJANGO_STATIC_URL=/assets/ \
	POKEMONTCG_IO_API_KEY= \
	$(BUILD_VENV)/bin/python backend/manage.py runserver

.PHONY: init-frontend
init-frontend:
	cd frontend && yarn install

.PHONY: run-frontend
run-frontend: 
	VITE_API_BASE_URL=http://localhost:8000/api/ \
	cd frontend && yarn dev