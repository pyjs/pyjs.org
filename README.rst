Welcome to the guts behind pyjs.org glory.

This repository contains the code for the http://pyjs.org website. (The actual content of the
website, as viewed online, is placed in the `pyjs.github.com <https://github.com/pyjs/pyjs.github.com>`_
repository, and is supposed to be a fully auto-generated thing: the webspace if you want so.)

Current State
=============

The website is a Pyjs application, driven by ~200 lines of code in website.py, some static files
in the public/ directory, and PageLoader.py that pulls the FAQs together from public/faq/answers/.

Planned Features
================

The content of the pyjs.org website should be pulled off of the wiki pages of this repository.
In other words, the website is supposed to be built afresh automatically each time a wiki page
is modified.

You can take a look at the ongoing work in build.py, and the template.html file.
