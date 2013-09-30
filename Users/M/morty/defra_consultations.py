import scraperwiki
import urllib2
from lxml import etree

dept_name = u'Department for Environment, Food and Rural Affairs'

def scrape_page(url):
    record = {u'URI': url,
              u'department': dept_name,
              u'agency': ''}

    documents = []

    html = scraperwiki.scrape(url)

    if html.count("Error 404"):
        raise Exception("404")

    doc = etree.HTML(html)

    record[u'title'] = doc.xpath('//h1[@property="dc:title"]')[0].text
    record[u'published_date'] = doc.xpath('//span[@property="dc:issued"]')[0].attrib['content']
    record[u'start_date'] = doc.xpath('//span[@property="dc:available"]')[0].attrib['content']
    record[u'end_date'] = doc.xpath('//span[@property="dc:valid"]')[0].attrib['content']
    record[u'description'] = etree.tostring(doc.xpath('//div[@property="dc:abstract"]')[0])
    record[u'sponsor'] = ''

    for doc in doc.xpath('//h2[contains(.,"Consultation documents")]/following-sibling::ul[1]/li/a'):
        href = doc.attrib['href']
        if href.startswith('/'):
            href = 'http://www.defra.gov.uk' + href
        documents.append({u'consultation': record[u'URI'], u'URI': href, u'title': doc.text})

    return record, documents

for consultation in scraperwiki.datastore.getData('directgov_consultations'):
    if consultation[u'department'] == dept_name:
        try:
            record, documents = scrape_page(consultation[u'permalink'])
            scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')
            for doc in documents:
                 scraperwiki.sqlite.save(['URI'], data=doc, table_name='documents')
        except Exception, ex:
            print ex
            continue
import scraperwiki
import urllib2
from lxml import etree

dept_name = u'Department for Environment, Food and Rural Affairs'

def scrape_page(url):
    record = {u'URI': url,
              u'department': dept_name,
              u'agency': ''}

    documents = []

    html = scraperwiki.scrape(url)

    if html.count("Error 404"):
        raise Exception("404")

    doc = etree.HTML(html)

    record[u'title'] = doc.xpath('//h1[@property="dc:title"]')[0].text
    record[u'published_date'] = doc.xpath('//span[@property="dc:issued"]')[0].attrib['content']
    record[u'start_date'] = doc.xpath('//span[@property="dc:available"]')[0].attrib['content']
    record[u'end_date'] = doc.xpath('//span[@property="dc:valid"]')[0].attrib['content']
    record[u'description'] = etree.tostring(doc.xpath('//div[@property="dc:abstract"]')[0])
    record[u'sponsor'] = ''

    for doc in doc.xpath('//h2[contains(.,"Consultation documents")]/following-sibling::ul[1]/li/a'):
        href = doc.attrib['href']
        if href.startswith('/'):
            href = 'http://www.defra.gov.uk' + href
        documents.append({u'consultation': record[u'URI'], u'URI': href, u'title': doc.text})

    return record, documents

for consultation in scraperwiki.datastore.getData('directgov_consultations'):
    if consultation[u'department'] == dept_name:
        try:
            record, documents = scrape_page(consultation[u'permalink'])
            scraperwiki.sqlite.save(['URI'], data=record, table_name='consultations')
            for doc in documents:
                 scraperwiki.sqlite.save(['URI'], data=doc, table_name='documents')
        except Exception, ex:
            print ex
            continue
