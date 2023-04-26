#!/bin/bash

dropdb imperium && createdb imperium && rm -rf web/pages/migrations && mkdir web/pages/migrations && touch web/pages/migrations/__init__.py && python web/manage.py migrate && python web/manage.py makemigrations && python web/manage.py migrate && python web/createsuperuser.py
