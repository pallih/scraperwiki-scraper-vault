import scraperwiki
import lxml.html

# Blank Python
pagebase = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/search?@lurl@=1372183742&accF=../tmp/Acc.479108.42325000.11915&minCount='
minCounts = [10*i for i in range(1039)]

for i in minCounts:
    pagename = pagebase + str(i)
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('td a'):
        linkpagename = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/' + a.attrib['href']
        linkpage = scraperwiki.scrape(linkpagename)
        pageroot = lxml.html.fromstring(page)
        text = pageroot.text_content()
        data = {'Text': text}
        scraperwiki.sqlite.save(unique_keys = 'Text', data = data)import scraperwiki
import lxml.html

# Blank Python
pagebase = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/search?@lurl@=1372183742&accF=../tmp/Acc.479108.42325000.11915&minCount='
minCounts = [10*i for i in range(1039)]

for i in minCounts:
    pagename = pagebase + str(i)
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('td a'):
        linkpagename = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/' + a.attrib['href']
        linkpage = scraperwiki.scrape(linkpagename)
        pageroot = lxml.html.fromstring(page)
        text = pageroot.text_content()
        data = {'Text': text}
        scraperwiki.sqlite.save(unique_keys = 'Text', data = data)import scraperwiki
import lxml.html

# Blank Python
pagebase = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/search?@lurl@=1372183742&accF=../tmp/Acc.479108.42325000.11915&minCount='
minCounts = [10*i for i in range(1039)]

for i in minCounts:
    pagename = pagebase + str(i)
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for link in pageroot.cssselect('td a'):
        linkpagename = 'http://toolkit.dialog.com.ezp-prod1.hul.harvard.edu/intranet/cgi/' + a.attrib['href']
        linkpage = scraperwiki.scrape(linkpagename)
        pageroot = lxml.html.fromstring(page)
        text = pageroot.text_content()
        data = {'Text': text}
        scraperwiki.sqlite.save(unique_keys = 'Text', data = data)