#Forked from http://scraperwiki.com/scrapers/soverign_states/ just to play with

pageurl = "http://en.wikipedia.org/wiki/Wikipedia:Archived_delete_debates"
import scraperwiki
import lxml.html


tree = lxml.html.parse(pageurl)


for a in tree.xpath('//td/b/a'):
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href']})

for a in tree:
    print a
    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href']})

findall('<li class="toclevel-1">')
