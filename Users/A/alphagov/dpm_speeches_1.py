import scraperwiki
from lxml import etree

def scrape_speech(url, date):
    doc = etree.HTML(scraperwiki.scrape(url))
    title = doc.xpath('//h1[@id="page-title"]')[0].text
    speech = "\n".join([etree.tostring(x) for x in doc.xpath('//h1[@id="page-title"]/following-sibling::*')])
    scraperwiki.sqlite.save(['permalink'], {'permalink': url, 'title': title, 'body': speech, 'given_on': date, 'minister_name': 'The Rt Hon Nick Clegg MP'})

base_url = 'http://www.dpm.cabinetoffice.gov.uk'

html = scraperwiki.scrape(base_url + '/speeches')
doc = etree.HTML(html)

while True:
    for speech in doc.xpath('//dt/a'):
        url = base_url + speech.attrib['href']
        date = speech.xpath('../following-sibling::*[1]//span[@class="date-display-single"]')[0].text.split(',')[1].strip()
        scrape_speech(url, date)

    try:
        html = scraperwiki.scrape(base_url + doc.xpath('//a[@title="Go to next page"]')[0].attrib['href'])
        doc = etree.HTML(html)
    except:
        break
import scraperwiki
from lxml import etree

def scrape_speech(url, date):
    doc = etree.HTML(scraperwiki.scrape(url))
    title = doc.xpath('//h1[@id="page-title"]')[0].text
    speech = "\n".join([etree.tostring(x) for x in doc.xpath('//h1[@id="page-title"]/following-sibling::*')])
    scraperwiki.sqlite.save(['permalink'], {'permalink': url, 'title': title, 'body': speech, 'given_on': date, 'minister_name': 'The Rt Hon Nick Clegg MP'})

base_url = 'http://www.dpm.cabinetoffice.gov.uk'

html = scraperwiki.scrape(base_url + '/speeches')
doc = etree.HTML(html)

while True:
    for speech in doc.xpath('//dt/a'):
        url = base_url + speech.attrib['href']
        date = speech.xpath('../following-sibling::*[1]//span[@class="date-display-single"]')[0].text.split(',')[1].strip()
        scrape_speech(url, date)

    try:
        html = scraperwiki.scrape(base_url + doc.xpath('//a[@title="Go to next page"]')[0].attrib['href'])
        doc = etree.HTML(html)
    except:
        break
