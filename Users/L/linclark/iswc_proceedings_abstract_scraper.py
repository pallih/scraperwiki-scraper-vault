import scraperwiki
import urllib
import urllib2
import urlparse
import lxml.etree, lxml.html
import re
import HTMLParser

scraperwiki.sqlite.attach("iswc_2011_program_schedule", "schedule");
#kr = scraperwiki.sqlite.select("* from schedule.swdata where title like '%Reasoners'");
#print kr[0]['start_time']

# Research track.
html = scraperwiki.scrape("http://iswc2011.semanticweb.org/program/research-papers/")

root = lxml.html.fromstring(html)
num = 0;

for div in root.cssselect(".floatbox .csc-default"):
    divId = div.get('id')
    h2 = div.cssselect("tr h2")
    if len(h2) > 0:
        num = num + 1;
        time = h2[0].text_content()
        h1 = div.cssselect("h1")
        session_name = h1[0].text_content()
        rows = div.cssselect("tr")
        session_chair = rows[1].text_content().replace('Session Chair: ', '')
        session_uri = 'http://data.semanticweb.org/conference/iswc/2011/sessions/research/' + str(num)
        del rows[0]
        del rows[0]
        for row in rows:
            a = row.cssselect("td a")
            paper_name = a[0].text_content()
            paper_url = 'http://iswc2011.semanticweb.org/' + a[0].get('href')

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

            # Get the room and time information
            sessionData = scraperwiki.sqlite.select("* from schedule.swdata where id like '%" + divId + "'")

            # Save research paper to the database.
            data = {}
            data['session_name'] = session_name
            data['session_start'] = sessionData[0]['start_time']
            data['session_end'] = sessionData[0]['end_time']
            data['session_day'] = sessionData[0]['day']
            data['session_room'] = sessionData[0]['room']
            data['session_chair'] = session_chair
            data['session_uri'] = session_uri
            data['paper_name'] = paper_name
            data['paper_url'] = paper_url
            data['abstract'] = abstract
            scraperwiki.sqlite.save(unique_keys=['paper_url'], data=data)