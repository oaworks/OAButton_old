.PHONY: test lessc

all: build

build: lessc

lessc:
	lessc oabutton/static/public/less/styles.less oabutton/static/public/css/styles.css


test:
	python manage.py test web bookmarklet metadata
