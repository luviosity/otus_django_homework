PYTHON  ?= python3
MANAGE   = cd app && $(PYTHON) manage.py

.PHONY: runserver makemigrations migrate

makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

runserver:
	$(MANAGE) runserver

createsuperuser:
	$(MANAGE) createsuperuser
