GIT_REMOTE_BASE = https://github.com/pyjs/

.PHONY: *

build: api site

api: clone_pyjs
	./build.py -v --api-only --pyjs-src=build/pyjs

site: clone_pyjsorgwiki
	./build.py -v --site-only --wiki-src=build/wiki
	cp site/About.html site/index.html

clone: clone_pyjs clone_pyjsorgwiki

clone_pyjs:
	test -d build/pyjs || git clone --depth 1 $(GIT_REMOTE_BASE)pyjs.git build/pyjs
	cd build/pyjs && git pull

clone_pyjsorgwiki:
	test -d build/wiki || git clone --depth 1 $(GIT_REMOTE_BASE)pyjs.org.wiki.git build/wiki
	cd build/wiki && git pull
