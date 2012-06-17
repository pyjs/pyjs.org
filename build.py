#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from optparse import OptionParser, OptionGroup
from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer
from epydoc import cli
from os.path import join, basename
import glob, re, shutil, sys

reWikiLink = re.compile('\[\[(.*?)\]\]')
def makeWikiLink(m):
    parts = m.group(1).split('|')
    name = link = parts[0]
    if len(parts) == 2:
        link = parts[1]
    return '`%s <%s.html>`_' % (name, link)

def makeTemplate(menu):
    menu = menu.replace('<li><strong>', '<li class="section">')
    menu = menu.replace('</strong></li>', '</li>')
    tpl = open('template.html', 'r').read()
    tpl = re.sub('<ul class="menu-list">.*?</ul>', menu, tpl, flags=re.DOTALL|re.MULTILINE)
    return tpl

reDocument = re.compile('^<div class="document".*?>(.*)</div>$', re.DOTALL)
def wikiToHTML(wikiFile):
    wiki = open(wikiFile, 'r').read()
    src = reWikiLink.sub(makeWikiLink, wiki)
    parts = publish_parts(src, writer_name='html4css1')
    body = parts['html_body'].encode('utf-8')
    html = reDocument.search(body).group(1)
    return html

def getWikiPages(opts):
    files = glob.glob(join(opts.wiki, '*.rest'))
    files.remove(join(opts.wiki, 'Home.rest')) # skip default github wiki page
    files.remove(join(opts.wiki, 'Menu.rest')) # handled seperately
    return files

reBody = re.compile('(^<div id="body">).*?(^</div>)', re.DOTALL|re.MULTILINE)
def writeHTML(html, tpl, outfile):
    final = reBody.sub(r'\1'+html+r'\2', tpl)
    f = open(outfile, 'w')
    f.write(final)
    f.close()

def generateSite(opts):
    log = cli.ConsoleLogger(opts.verbosity)
    log.start_progress('Generating Website')

    menu = wikiToHTML(join(opts.wiki, 'Menu.rest'))
    template = makeTemplate(menu)

    wikiPages = getWikiPages(opts)
    nfiles = float(len(wikiPages))
    for i, page in enumerate(wikiPages):
        name = basename(page)[:-5]
        outname = join(opts.target, name+'.html')
        log.progress(i/nfiles, outname)
        html = wikiToHTML(page)
        writeHTML(html, template, outname)

    log.end_progress()

def generateAPI(opts):
    sys.argv = ['-v' for i in range(opts.verbosity)]
    sys.argv += [
        '--parse-only',
        '--name', 'Pyjs',
        '--url', 'http://pyjs.org',
        '-o', join(opts.target, 'api'),
        '--exclude', 'pyjamas.raphael',
        '--exclude', 'pyjamas.selection',
        '--exclude', 'pyjamas.chart',
        '--exclude', 'pyjamas.Canvas',
        join(opts.pyjs, 'library/pyjamas')
    ]
    cli.cli()

def getOptionParser():
    o = OptionParser(usage='%prog [options]')

    o.add_option("--output", "-o",
        dest="target", metavar="PATH", default="site",
        help="The output directory.")

    o.add_option("--wiki-src",
        dest="wiki", metavar="PATH", default="wiki",
        help="Wiki source directory.")

    o.add_option("--pyjs-src",
        dest="pyjs", metavar="PATH", default="../pyjs",
        help="Pyjs source directory.")

    o.add_option("--api-only",
        action="store_false", dest="site", default=True,
        help="Only generate the API docs.")

    o.add_option("--site-only",
        action="store_false", dest="api", default=True,
        help="Only generate the site.")

    o.add_option("--verbose", "-v",
        action="count", dest="verbosity", default=1,
        help="Increase the verbosity.")

    return o

if __name__ == "__main__":
    opts = getOptionParser().parse_args()[0]
    if opts.api: generateAPI(opts)
    if opts.site: generateSite(opts)
