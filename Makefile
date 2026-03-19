PYTHON  ?= python3
MANAGE  ?= $(PYTHON) manage.py

.PHONY: runserver makemigrations migrate

makemigrations:
    $(MANAGE) makemigrations
migrate:
    $(MANAGE) migrate
runserver:
    $(MANAGE) runserver
