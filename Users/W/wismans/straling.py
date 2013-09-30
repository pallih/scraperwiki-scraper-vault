from pyPdf import PdfFileWriter, PdfFileReader
import base64
from lxml import html, etree
import scraperwiki
from urlparse import urljoin
# ik wil eerst naar het overzicht van jaren
site = "http://www.senternovem.nl/stralingsbescherming/verleende_vergunningen/index.asp"
page = scraperwiki.scrape(site)
page = html.fromstring(page)
    
# dan wil ik per jaar gaan zoeken
for year in page.cssselect ("a.content"):
    url = year.get("href")
    url = urljoin(site, url)
    page = scraperwiki.scrape(url)
    page = html.fromstring(page)
    for year in page.cssselect("a.content"):
        url2 = year.get("href")
        url2 = urljoin(url, url2)
        page = scraperwiki.scrape(url2)
        page = html.fromstring(page)
        for year in page.cssselect("a.content"):
            url3 = year.get("href")
            url3 = urljoin(url2, url3)
            page = scraperwiki.scrape(url3)
            pdfxml = etree.XML(scraperwiki.pdftoxml(page))
            pdftext = etree.tostring(pdfxml, method='text', encoding="UTF-8")
            for kopje in pdfxml.xpath("//text[@font=\"1\"]"):
                print etree.tostring(kopje)
            data = {"url": url3, "document":base64.b64encode(page)}
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)from pyPdf import PdfFileWriter, PdfFileReader
import base64
from lxml import html, etree
import scraperwiki
from urlparse import urljoin
# ik wil eerst naar het overzicht van jaren
site = "http://www.senternovem.nl/stralingsbescherming/verleende_vergunningen/index.asp"
page = scraperwiki.scrape(site)
page = html.fromstring(page)
    
# dan wil ik per jaar gaan zoeken
for year in page.cssselect ("a.content"):
    url = year.get("href")
    url = urljoin(site, url)
    page = scraperwiki.scrape(url)
    page = html.fromstring(page)
    for year in page.cssselect("a.content"):
        url2 = year.get("href")
        url2 = urljoin(url, url2)
        page = scraperwiki.scrape(url2)
        page = html.fromstring(page)
        for year in page.cssselect("a.content"):
            url3 = year.get("href")
            url3 = urljoin(url2, url3)
            page = scraperwiki.scrape(url3)
            pdfxml = etree.XML(scraperwiki.pdftoxml(page))
            pdftext = etree.tostring(pdfxml, method='text', encoding="UTF-8")
            for kopje in pdfxml.xpath("//text[@font=\"1\"]"):
                print etree.tostring(kopje)
            data = {"url": url3, "document":base64.b64encode(page)}
            scraperwiki.sqlite.save(unique_keys=["url"], data=data)