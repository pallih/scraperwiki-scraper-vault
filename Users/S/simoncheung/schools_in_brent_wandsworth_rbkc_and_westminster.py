import scraperwiki
import lxml.html
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
                raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.triedEncodings))
    return converted.unicode

for lea in ['Brent', 'Westminster', 'Hammersmith+and+Fulham', 'Wandsworth']:
    indexpage = scraperwiki.scrape('http://schoolswebdirectory.co.uk/leasearch.php?lea={0}&where=4&submit=Submit'.format(lea))
    doc = lxml.html.fromstring(decode_html(indexpage))
    doc.make_links_absolute('http://schoolswebdirectory.co.uk/')
    for link in doc.cssselect('a'):
        if link.text == 'info':
            url = link.get('href')
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)

            data = dict()
            for tr in root.cssselect(".rc_infobox tr"):
                tds = tr.cssselect("td")
                if len(tds)==2:
                    name=tds[0].text_content().strip().replace(':','').replace('/Principal','')
                    value=tds[1].text_content().strip()
                    if len(name)>0:
                        data[name]=value

            scraperwiki.sqlite.save(unique_keys=['School'], data=data)import scraperwiki
import lxml.html
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
                raise UnicodeDecodeError(
                "Failed to detect encoding, tried [%s]",
                ', '.join(converted.triedEncodings))
    return converted.unicode

for lea in ['Brent', 'Westminster', 'Hammersmith+and+Fulham', 'Wandsworth']:
    indexpage = scraperwiki.scrape('http://schoolswebdirectory.co.uk/leasearch.php?lea={0}&where=4&submit=Submit'.format(lea))
    doc = lxml.html.fromstring(decode_html(indexpage))
    doc.make_links_absolute('http://schoolswebdirectory.co.uk/')
    for link in doc.cssselect('a'):
        if link.text == 'info':
            url = link.get('href')
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)

            data = dict()
            for tr in root.cssselect(".rc_infobox tr"):
                tds = tr.cssselect("td")
                if len(tds)==2:
                    name=tds[0].text_content().strip().replace(':','').replace('/Principal','')
                    value=tds[1].text_content().strip()
                    if len(name)>0:
                        data[name]=value

            scraperwiki.sqlite.save(unique_keys=['School'], data=data)