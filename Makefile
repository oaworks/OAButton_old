.PHONY: test

all: build

build:



test:
	python manage.py test web bookmarklet metadata
