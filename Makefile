GIT_REMOTE_BASE = https://github.com/pyjs/

.PHONY: *

build: update site api examples

update:
	git pull

examples: clone_pyjs
	python2 build/pyjs/examples/__main__.py --download
	mv build/pyjs/examples/__output__ site/examples

api: clone_pyjs
	mkdir -p site/api
	python2 build.py -v --api-only --pyjs-src=build/pyjs

site: clone_pyjsorgwiki
	mkdir -p site
	python2 build.py -v --site-only --wiki-src=build/wiki
	cp site/About.html site/index.html

clone_pyjs:
	test -d build/pyjs || git clone --depth 1 $(GIT_REMOTE_BASE)pyjs.git build/pyjs
	cd build/pyjs && git pull

clone_pyjsorgwiki:
	test -d build/wiki || git clone --depth 1 $(GIT_REMOTE_BASE)pyjs.org.wiki.git build/wiki
	cd build/wiki && git pull

#-----------------------------------------------------------------( end build )

distclean:
	git clean -ffdx

clean:
	git clean -fdxe /build
