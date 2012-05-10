.PHONY: *

build:
	./build.py -v
	cp site/About.html site/index.html

api:
	./build.py -v --api-only

site:
	./build.py -v --site-only
	cp site/About.html site/index.html
