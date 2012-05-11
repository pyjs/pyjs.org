GIT_REMOTE_BASE = https://github.com/pyjs/

.PHONY: *

build: update site api

update:
	git pull

examples: clone_pyjs
	mkdir -p site/examples
	#XXX translate ALL examples to ONE location
	# without merging the translated modules, the examples dir is over 500MiB ... far too large for Github,
	# and is unacceptable anyways. the solution is to use --multi-file, thereby allowing all examples
	# to share dynamic_app_modules ... however, we also want --compile-inplace else our compile time will be
	# *exponentially* longer. these two are currently mutually exclusive for no good reason [f0e22a04];
	# a long standing bug (gc#533) prevents `cp {src}/lib.js  {out}/lib/`, AND mangles the mod names in the
	# cache.html loader ... the app fails before it even starts. this was never fixed because the current
	# linker/visitor doesn't keep very good track of modules -- it uses path/module-name/module-path/???, .PY
	# AND .JS -- and there is no foolproof way to convert the fullpath (what we see), to an abs import name +
	# platform (how stuff is stored in lib/).
	#
	# ... fix by introducing proper(!) OO design, and mirroring real python modules:
	#
	# x_sys = type('x_sys', (x_module,), {'x_file': '/abs/.../me.py',
	#                                     'x_name': 'my.super.module',
	#                                     'x_path': ['/where/to/find/more'],
	#                                      ?????? : [...]})
	#
	# ... this way you retain -- and have access too -- all infomation whenever it's needed. this should also
	# simplify MUCH of the translation process.
	#
	#python2 build/pyjs/examples/__main__.py --download -- --multi-file --cache-buster --compile-inplace
	cp -a build/pyjs/examples/[^_]*/ site/examples

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
