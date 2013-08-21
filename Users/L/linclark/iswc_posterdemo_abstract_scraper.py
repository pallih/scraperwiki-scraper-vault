import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

#scraperwiki.sqlite.attach("iswc_2011_program_schedule", "schedule");

# In Use track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/posters-and-demos/")

root = lxml.html.fromstring(html)

divs = root.cssselect(".floatbox .csc-default")[0:2]
for div in divs:
    tr = div.cssselect('tr')
    for row in tr[1:]:
        td = row.cssselect('td')
        a = td[2].cssselect('a')
        for paper in a:
            paper_name = paper.text_content()
            paper_url = 'http://iswc2011.semanticweb.org/' + paper.get('href').lstrip('../')

            pdfdata = urllib.urlopen(paper_url).read()
            pdfxml = scraperwiki.pdftoxml(pdfdata)
            # If a paper uses special characters, lxml will break. Print out the names and do them manually
            try:
                pdfRoot = lxml.etree.fromstring(pdfxml)
                inAbstract = False;
                abstract = '';

                for page in pdfRoot:
                    assert page.tag == 'page'
                    pagelines = { }
                    for v in page:
                        if v.tag == 'text':
                            text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)   # there has to be a better way here to get the contents
                            if re.search('Abstract.', text):
                                inAbstract = True
                            if re.search('Keywords', text) or re.search('Introduction', text):
                                inAbstract = False
                            if inAbstract:
                                abstract = abstract + ' ' + text
                    break;
            except:
                abstract = 'Error'
            
            # Unescape the abstract, which has HTML char codes.
            h = HTMLParser.HTMLParser()
            abstract = h.unescape(abstract)

            # Save paper to the database.
            data = {}
            data['abstract'] = abstract
            data['paper_name'] = paper_name
            data['paper_url'] = paper_url
            scraperwiki.sqlite.save(unique_keys=['paper_url'], data=data)
