"""Retrieves the Source and Destination station pairs for APSRTC buses
"""
from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://www.apsrtconline.in/'
sources = dict()

def get_sources():
    html = scraperwiki.scrape(base_url)
    assert 'APSRTC Official Website' in html
    root = lxml.html.fromstring(html)
    for option in root.cssselect('select[name=source] option'):
        id = option.get('value')
        if not id:
            continue
        name = str(option.text_content()).strip()
        sources[id] = name


def get_destinations():
    for source_id in sources:
        print "Fetching destinations for", source_id
        url = base_url + 'getdestinations.php?sourceid=' + source_id
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        data = []
        for option in root.cssselect('select[name=destination] option'):
            destination_id = option.get('value')
            if not destination_id:
                continue
            destination_name = str(option.text_content()).strip()
            data.append(dict(source_id=source_id,
                             source_name=sources[source_id],
                             destination_id=destination_id,
                             destination_name=destination_name))

        scraperwiki.sqlite.save(data=data,
                                unique_keys=['source_name',
                                             'destination_name'])


def main():
    get_sources()
    get_destinations()


main()"""Retrieves the Source and Destination station pairs for APSRTC buses
"""
from datetime import datetime
import re
import scraperwiki
import lxml.html

base_url = 'http://www.apsrtconline.in/'
sources = dict()

def get_sources():
    html = scraperwiki.scrape(base_url)
    assert 'APSRTC Official Website' in html
    root = lxml.html.fromstring(html)
    for option in root.cssselect('select[name=source] option'):
        id = option.get('value')
        if not id:
            continue
        name = str(option.text_content()).strip()
        sources[id] = name


def get_destinations():
    for source_id in sources:
        print "Fetching destinations for", source_id
        url = base_url + 'getdestinations.php?sourceid=' + source_id
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        data = []
        for option in root.cssselect('select[name=destination] option'):
            destination_id = option.get('value')
            if not destination_id:
                continue
            destination_name = str(option.text_content()).strip()
            data.append(dict(source_id=source_id,
                             source_name=sources[source_id],
                             destination_id=destination_id,
                             destination_name=destination_name))

        scraperwiki.sqlite.save(data=data,
                                unique_keys=['source_name',
                                             'destination_name'])


def main():
    get_sources()
    get_destinations()


main()