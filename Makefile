.PHONY: test test_js test_py lessc

all: build

build: lessc

lessc:
	lessc oabutton/static/public/less/styles.less oabutton/static/public/css/styles.css


test: test_js test_py

test_py:
	python manage.py test web bookmarklet metadata

test_js:
	phantomjs scripts/qunit-runner.js oabutton/static/test/test.html
