import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")

root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data


"""
pagename = 'http://www.socaltech.com/intelligence/index.php?action=dopowersearch&searchtype=company&coname=&keywords1=&companytype=0&companyarea=2&subarea=0&industry%5B%5D=6&city=0&state=0&zip='

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
"""