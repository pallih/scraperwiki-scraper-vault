import os
import re
import tempfile
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import datetime
import scraperwiki.sqlite as db

Now = datetime.datetime.now()

VERBOSE_SAVE = 0


def process_pdf(url):
    data = pdftotext(scraperwiki.scrape(url))
    #print data
    for line in data.splitlines():
        columns = re.split(r'\s{2,}', line)
        print columns
        if len(columns) < 30:
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
    print text


g_entry_id = 0
def save_entry(entry):
    global g_entry_id
    entry['id'] = g_entry_id
    g_entry_id += 1
    db.save(['id'], data=entry, verbose=VERBOSE_SAVE)


## MAIN
#for link in iter_pdf_links():
   # process_pdf(link)   


html = scraperwiki.scrape('http://www.stoke.gov.uk/ccm/content/business/general/procurement/current-tender-and-quotation-opportunities.en/')
base_url ='http://www.stoke.gov.uk'
root2 = lxml.html.fromstring(html) # turn our HTML into an lxml object
for link in root2.cssselect("li.attachment-link a"):
    ext_link = link.attrib['href']
    #print ext_link
    url = base_url+ext_link  
    print url
    process_pdf(url)
import os
import re
import tempfile
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import datetime
import scraperwiki.sqlite as db

Now = datetime.datetime.now()

VERBOSE_SAVE = 0


def process_pdf(url):
    data = pdftotext(scraperwiki.scrape(url))
    #print data
    for line in data.splitlines():
        columns = re.split(r'\s{2,}', line)
        print columns
        if len(columns) < 30:
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
    print text


g_entry_id = 0
def save_entry(entry):
    global g_entry_id
    entry['id'] = g_entry_id
    g_entry_id += 1
    db.save(['id'], data=entry, verbose=VERBOSE_SAVE)


## MAIN
#for link in iter_pdf_links():
   # process_pdf(link)   


html = scraperwiki.scrape('http://www.stoke.gov.uk/ccm/content/business/general/procurement/current-tender-and-quotation-opportunities.en/')
base_url ='http://www.stoke.gov.uk'
root2 = lxml.html.fromstring(html) # turn our HTML into an lxml object
for link in root2.cssselect("li.attachment-link a"):
    ext_link = link.attrib['href']
    #print ext_link
    url = base_url+ext_link  
    print url
    process_pdf(url)
