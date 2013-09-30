import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

# DC track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/doctoral-consortium/")

root = lxml.html.fromstring(html)
num = 0;

for row in root.cssselect("#c1529 tr"):
    td = row.cssselect('td')
    if td[0].get('rowspan') > 0 and td[0].get('rowspan') != '1':
        num = num + 1
        split = td[0].text_content().split('-')
        startTime = split[0].strip()
        endTime = split[1].strip()
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/doctoral-consortium/' + str(num)
        
    if re.search('DC Prop', td[-1].text_content()):
        paper_name = td[-1].text_content()
        paper_url = 'http://iswc2011.semanticweb.org/' + td[-1].cssselect('a')[0].get('href').lstrip('../')

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
                break
        except:
            abstract = 'Error'
            
        # Unescape the abstract, which has HTML char codes.
        h = HTMLParser.HTMLParser()
        abstract = h.unescape(abstract)

        # Save research paper to the database.
        data = {}
        data['session_start'] = startTime
        data['session_end'] = endTime
        data['session_day'] = 'Monday'
        data['session_room'] = 'Einstein'
        data['session_uri'] = session_uri
        data['paper_name'] = paper_name
        data['paper_url'] = paper_url
        data['abstract'] = abstract
        scraperwiki.sqlite.save(unique_keys=['paper_url'], data=data)import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

# DC track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/doctoral-consortium/")

root = lxml.html.fromstring(html)
num = 0;

for row in root.cssselect("#c1529 tr"):
    td = row.cssselect('td')
    if td[0].get('rowspan') > 0 and td[0].get('rowspan') != '1':
        num = num + 1
        split = td[0].text_content().split('-')
        startTime = split[0].strip()
        endTime = split[1].strip()
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/doctoral-consortium/' + str(num)
        
    if re.search('DC Prop', td[-1].text_content()):
        paper_name = td[-1].text_content()
        paper_url = 'http://iswc2011.semanticweb.org/' + td[-1].cssselect('a')[0].get('href').lstrip('../')

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
                break
        except:
            abstract = 'Error'
            
        # Unescape the abstract, which has HTML char codes.
        h = HTMLParser.HTMLParser()
        abstract = h.unescape(abstract)

        # Save research paper to the database.
        data = {}
        data['session_start'] = startTime
        data['session_end'] = endTime
        data['session_day'] = 'Monday'
        data['session_room'] = 'Einstein'
        data['session_uri'] = session_uri
        data['paper_name'] = paper_name
        data['paper_url'] = paper_url
        data['abstract'] = abstract
        scraperwiki.sqlite.save(unique_keys=['paper_url'], data=data)