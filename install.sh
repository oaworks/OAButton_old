#!/bin/sh
mkvirtualenv oabutton-py
pip install -r requirements.txt
cd oabutton
python manage.py syncdb
python manage.py runserver
