all:
	mkvirtualenv oabutton-py
	workon oabutton-py
	pip install -r requirements.txt
	python manage.py syncdb
	python manage.py runserver

freeze:
	# Freeze the virtualenv setup
	pip freeze > requirements.txt


