import scraperwiki
import lxml.html

# Blank Python

pagename = 'http://www.presidency.ucsb.edu/sou.php'

page = scraperwiki.scrape(pagename)
pageroot = lxml.html.fromstring(page)

for link in pageroot.cssselect('td.doclist a'):
    linkname = link.attrib['href']
    if linkname[0:10] == 'http://www':
        linkpage = scraperwiki.scrape(linkname)
        linkpageroot = lxml.html.fromstring(linkpage)
        for d in linkpageroot.cssselect('span.docdate'):
            date = d.text
        speech = ''
        for s in linkpageroot.cssselect('span.displaytext'):
            speech = speech + s.text_content()
        data = {'Date': date, 'Speech': speech}
        scraperwiki.sqlite.save(unique_keys = ['Speech'], data = data)
    