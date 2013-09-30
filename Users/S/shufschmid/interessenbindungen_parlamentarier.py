import scraperwiki
import lxml.html
from unidecode import unidecode
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode


html = scraperwiki.scrape("http://www.parlament.ch/D/ORGANE-MITGLIEDER/NATIONALRAT/MITGLIEDER-NR-A-Z/Seiten/default.aspx")
root = lxml.html.fromstring(decode_html(html))
neu = 0
id = 0
for el in root.cssselect("ul.profilelist ul.linklist"):
        einzel = el.cssselect("a")[0]
        if neu == 0:
            neu = 1
        else:
            url = "http://www.parlament.ch"+einzel.attrib['href']
            name = einzel.attrib['title']
            name_decoded = unidecode(name[14:-7])
            egal, nummer = url.split('=')
            
            bio = scraperwiki.scrape(url)
            inhalt = lxml.html.fromstring(decode_html(bio))
            for elemente in inhalt.cssselect("table.standardtable tr.borderbottom"):
                verbindungen = elemente[0].text
                verbindungen_decoded = unidecode(verbindungen)
                id += 1
                data = {
                    'id' : id,
                    'name' : name_decoded,
                    'nummer' : nummer,
                    'verbindungen' : verbindungen_decoded
                }
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
                
            neu = 0


            
import scraperwiki
import lxml.html
from unidecode import unidecode
from BeautifulSoup import UnicodeDammit

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode


html = scraperwiki.scrape("http://www.parlament.ch/D/ORGANE-MITGLIEDER/NATIONALRAT/MITGLIEDER-NR-A-Z/Seiten/default.aspx")
root = lxml.html.fromstring(decode_html(html))
neu = 0
id = 0
for el in root.cssselect("ul.profilelist ul.linklist"):
        einzel = el.cssselect("a")[0]
        if neu == 0:
            neu = 1
        else:
            url = "http://www.parlament.ch"+einzel.attrib['href']
            name = einzel.attrib['title']
            name_decoded = unidecode(name[14:-7])
            egal, nummer = url.split('=')
            
            bio = scraperwiki.scrape(url)
            inhalt = lxml.html.fromstring(decode_html(bio))
            for elemente in inhalt.cssselect("table.standardtable tr.borderbottom"):
                verbindungen = elemente[0].text
                verbindungen_decoded = unidecode(verbindungen)
                id += 1
                data = {
                    'id' : id,
                    'name' : name_decoded,
                    'nummer' : nummer,
                    'verbindungen' : verbindungen_decoded
                }
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
                
            neu = 0


            
