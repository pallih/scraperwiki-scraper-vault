from os import linesep

from lxml import html
import scraperwiki

root = 'http://preview.grid.unep.ch/index.php?preview=data&lang=eng'


def normalise_key(key):
    return key.strip(':').strip().lower().replace(' ', '_').replace('.','_')

def normalise_val(val):
    val = val.strip()
    if val == '---':
        return None
    return val

def go(url):
        page = html.document_fromstring(scraperwiki.scrape(url))
        headings = page.cssselect('div.Text2 strong')
        if len(headings) > 1:
            yield headings[1].text
            key = ''
            vals = []
            for metadata in page.cssselect('div#metadata div.Text'):
                if metadata[0].tag == 'strong':
                    if key and vals:
                        yield key, linesep.join(vals)
                        vals = []
                    key = metadata[0].text_content().strip()
                    try:
                        vals.append(metadata[1].text_content().strip())
                    except IndexError: pass
                else:
                    print metadata.text.strip(), metadata[0].text_content()
                    vals.append(metadata.text + metadata[0].text_content().strip())
                
            for img in page.cssselect('a img'):
                try:
                    webservice = img.getparent()
                    url = webservice.attrib['href']
                    if url !='rss/preview.xml':
                        webservice_type=img.attrib['alt']
                        yield webservice_type, url
                except IndexError:
                    pass
                except KeyError:
                    msg = html.tostring(webservice)
                    if not 'onclick' in msg:
                        print 'ERR', msg, url

def main():
    for event_type in ('cyclones', 'surge', 'droughts', 'fires', 'floods', 'landslides', 'tsunamis', 'volcanoes', 'earthquakes', 'multiple'):
        for cat in range(1, 9):
            url = "http://preview.grid.unep.ch/index.php?preview=data&events=" + event_type + "&evcat=" + str(cat) + "&lang=eng"
            print 'STARTING', url
            dataset = {}
            for event in go(url):
                print event
                key, val = normalise_key(event[0]), normalise_val(event[1])
                dataset[key] = val
            if dataset:
                dataset['uri'] = url
                scraperwiki.sqlite.save(['uri'], dataset, table_name='datasets')

main()
from os import linesep

from lxml import html
import scraperwiki

root = 'http://preview.grid.unep.ch/index.php?preview=data&lang=eng'


def normalise_key(key):
    return key.strip(':').strip().lower().replace(' ', '_').replace('.','_')

def normalise_val(val):
    val = val.strip()
    if val == '---':
        return None
    return val

def go(url):
        page = html.document_fromstring(scraperwiki.scrape(url))
        headings = page.cssselect('div.Text2 strong')
        if len(headings) > 1:
            yield headings[1].text
            key = ''
            vals = []
            for metadata in page.cssselect('div#metadata div.Text'):
                if metadata[0].tag == 'strong':
                    if key and vals:
                        yield key, linesep.join(vals)
                        vals = []
                    key = metadata[0].text_content().strip()
                    try:
                        vals.append(metadata[1].text_content().strip())
                    except IndexError: pass
                else:
                    print metadata.text.strip(), metadata[0].text_content()
                    vals.append(metadata.text + metadata[0].text_content().strip())
                
            for img in page.cssselect('a img'):
                try:
                    webservice = img.getparent()
                    url = webservice.attrib['href']
                    if url !='rss/preview.xml':
                        webservice_type=img.attrib['alt']
                        yield webservice_type, url
                except IndexError:
                    pass
                except KeyError:
                    msg = html.tostring(webservice)
                    if not 'onclick' in msg:
                        print 'ERR', msg, url

def main():
    for event_type in ('cyclones', 'surge', 'droughts', 'fires', 'floods', 'landslides', 'tsunamis', 'volcanoes', 'earthquakes', 'multiple'):
        for cat in range(1, 9):
            url = "http://preview.grid.unep.ch/index.php?preview=data&events=" + event_type + "&evcat=" + str(cat) + "&lang=eng"
            print 'STARTING', url
            dataset = {}
            for event in go(url):
                print event
                key, val = normalise_key(event[0]), normalise_val(event[1])
                dataset[key] = val
            if dataset:
                dataset['uri'] = url
                scraperwiki.sqlite.save(['uri'], dataset, table_name='datasets')

main()
