#!/usr/bin/env python

from docutils.core import publish_parts
from docutils.writers.html4css1 import Writer
import glob, re

reWikiLink = re.compile('\[\[(.*?)\]\]')
def makeWikiLink(m):
    parts = m.group(1).split('|')
    name = link = parts[0]
    if len(parts) == 2:
        link = parts[1]
    return '`%s <%s.html>`_' % (name, link)

reBody = re.compile('(^<div id="body">).*?(^</div>)', re.DOTALL|re.MULTILINE)
def writeDocument(html, tpl, outfile):
    final = reBody.sub(r'\1'+html+r'\2', tpl)
    f = open(outfile, 'w')
    f.write(final)
    f.close()

def makeTemplate(menu):
    menu = menu.replace('<li><strong>', '<li class="section">')
    menu = menu.replace('</strong></li>', '</li>')
    tpl = open('template.html', 'r').read()
    tpl = re.sub('<ul class="menu-list">.*?</ul>', menu, tpl, flags=re.DOTALL|re.MULTILINE)
    return tpl

reDocument = re.compile('^<div class="document".*?>(.*)</div>$', re.DOTALL)
def getRenderedPages():
    pages = {}
    files = glob.glob('*.rest')
    for fname in files:
        wiki = open(fname, 'r').read()
        src = reWikiLink.sub(makeWikiLink, wiki)
        parts = publish_parts(src, writer_name='html4css1')
        body = parts['html_body'].encode('utf-8')
        html = reDocument.search(body).group(1)
        pages[fname[:-5]] = html
    return pages

if __name__ == "__main__":
    pages = getRenderedPages()
    menu = pages.pop('Menu')
    template = makeTemplate(menu)
    for name, page in pages.items():
        writeDocument(page, template, name+'.html')
