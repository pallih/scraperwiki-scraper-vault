import os
import re
import tempfile

import scraperwiki
import lxml.html
import scraperwiki.sqlite as db


VERBOSE_SAVE = 0
source_url = 'http://www.bbc.co.uk/news/uk-17358291'
test_url = 'http://news.bbc.co.uk/1/shared/bsp/hi/pdfs/19_03_12_day1_landsend_plymouth.pdf'


def iter_pdf_links(url):
    doc = lxml.html.fromstring(scraperwiki.scrape(url))
    for href in doc.xpath('//a[contains(@href, ".pdf")]/@href'):
        yield href
        # return  # not oneliner for debugging purposes


def process_pdf(url):
    data = pdftotext(scraperwiki.scrape(url))
    for line in data.splitlines():
        columns = re.split(r'\s{2,}', line)
        if len(columns) < 3:
            continue
        if not re.match(r'\d+', columns[0]):
            continue
        entry = {'day': int(columns[0])}
        community_idx = 1
        if len(columns) == 4:
            entry['time'] = columns[1]
            community_idx = 2
        entry['community'] = columns[community_idx]
        entry['travelling_on'] = columns[community_idx + 1]
        save_entry(entry)    


# taken from https://scraperwiki.com/scrapers/pdf_to_text_-_example_of_how_to_do_it/
def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -layout -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    return text


g_entry_id = 0
def save_entry(entry):
    global g_entry_id
    entry['id'] = g_entry_id
    g_entry_id += 1
    db.save(['id'], data=entry, verbose=VERBOSE_SAVE)


## MAIN
for link in iter_pdf_links():
    process_pdf(link)   



