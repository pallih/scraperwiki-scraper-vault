import scraperwiki
import lxml.html
import urllib2

#Scrape bribe docs

base = 'http://www.ipaidabribe.com/all-reports?page='

for i in range(1256,1776): #npages + 1
    pagename = base + str(i)
    page = scraperwiki.scrape(pagename)
    pageroot = lxml.html.fromstring(page)
    for l in pageroot.cssselect('div.paid-report-content > div.teaser-title a'):
        link = l.attrib['href']
        stem = 'http://www.ipaidabribe.com'
        docpagename = stem + link
        try:
            docpage = scraperwiki.scrape(docpagename)
            docpageroot = lxml.html.fromstring(docpage)
            for h in docpageroot.cssselect('div.pbr-top-pane> h2.node-title'):
                title = h.text_content()
            for p in docpageroot.cssselect('div.pbr-top-pane > p.pbr-default'):
                summary = p.text_content()
            for f in docpageroot.cssselect('span.pbr-to-whom'):
                info = f.text_content()
            for d in docpageroot.cssselect('span.pbr-posted'):
                date = d.text_content()
            amount = ''
            for a in docpageroot.cssselect('span.pbr-price'):
                amount = a.text_content()
            place = ''
            for l in docpageroot.cssselect('div#Most-Viewed-block span'):
                place += l.text_content()
            data = {'Summary': summary, 'Title': title, 'To Whom': info, 'Date': date, 'Amount': amount, 'Place': place}
            scraperwiki.sqlite.save(unique_keys = ['Summary'], data = data)
        except urllib2.HTTPError:
            continue
        except NameError:
            print link

