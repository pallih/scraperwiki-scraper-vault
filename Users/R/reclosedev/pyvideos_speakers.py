import scraperwiki.sqlite as db
import string
from collections import defaultdict

import lxml.html
import requests



def iter_docs():
    for letter in string.ascii_lowercase:
        r = requests.get('http://pyvideo.org/speaker/?character=%s' % letter)
        if r.ok:
            yield lxml.html.fromstring(r.text)


def speakers_from_doc(doc):
    entry_xpath = '//table[@class="table"]//td/%s'
    for pubs, speaker, href in zip(doc.xpath(entry_xpath % 'a'), 
                                   doc.xpath(entry_xpath % 'a/text()'), 
                                   doc.xpath(entry_xpath % 'a/@href')):
        yield int(pubs.tail.strip().strip('(').strip(')')), speaker, href


records = []
for doc in iter_docs():
    for pubs, speaker, href in speakers_from_doc(doc):
        records.append({'pubs': pubs, 'speaker': speaker, 'href': href})


db.execute("drop table if exists swdata")
db.save(['href'], records)
import scraperwiki.sqlite as db
import string
from collections import defaultdict

import lxml.html
import requests



def iter_docs():
    for letter in string.ascii_lowercase:
        r = requests.get('http://pyvideo.org/speaker/?character=%s' % letter)
        if r.ok:
            yield lxml.html.fromstring(r.text)


def speakers_from_doc(doc):
    entry_xpath = '//table[@class="table"]//td/%s'
    for pubs, speaker, href in zip(doc.xpath(entry_xpath % 'a'), 
                                   doc.xpath(entry_xpath % 'a/text()'), 
                                   doc.xpath(entry_xpath % 'a/@href')):
        yield int(pubs.tail.strip().strip('(').strip(')')), speaker, href


records = []
for doc in iter_docs():
    for pubs, speaker, href in speakers_from_doc(doc):
        records.append({'pubs': pubs, 'speaker': speaker, 'href': href})


db.execute("drop table if exists swdata")
db.save(['href'], records)
