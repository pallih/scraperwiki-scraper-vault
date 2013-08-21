import scraperwiki
import lxml.etree
import lxml.html

LAST_MONTH = 0
BASE_URL = 'http://www.gazzettaufficiale.it'
DEBUG = 0

def scrape_gu(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    t = root.cssselect("span[class='estremi']")
    gazzetta = "GU n. " + t[0].text + " del " + t[1].text

    for i in root.cssselect(".risultato"):
        if "coop." in i[1].text or "Coop." in i[1].text or "Cooperativ" in i[1].text or "cooperativ" in i[1].text:
            record = {
                "gazz" : gazzetta,
                "titolo" : i[1].text.strip().replace("\n", " "),
                "provv" : i.cssselect('.data')[0].text.strip().replace("\n", " "),
                "pag" : i.cssselect('.pagina')[0].text.strip().replace("\n", " "),
                "link" : BASE_URL + i[1].attrib['href'],
            }
            if DEBUG == 1:
                print i[1].text.strip().replace("\n", " ")
            else:
                scraperwiki.sqlite.save(unique_keys=["titolo"], data=record)


if LAST_MONTH == 1:
    gu_html = scraperwiki.scrape('http://www.gazzettaufficiale.it/30giorni/serie_generale')
    gu_root = lxml.html.fromstring(gu_html)

    for i in gu_root.cssselect(".elenco_ugazzette"):
        scrape_gu(BASE_URL + i.attrib['href'])

else:
    gu_html = scraperwiki.scrape(BASE_URL)
    gu_root = lxml.html.fromstring(gu_html)
    url = gu_root.cssselect(".ultimelist li a")[0].attrib['href']
    scrape_gu(BASE_URL + url)

