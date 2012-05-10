.PHONY: *

build:
	./build.py -v

api:
	./build.py -v --api-only

site:
	./build.py -v --site-only
