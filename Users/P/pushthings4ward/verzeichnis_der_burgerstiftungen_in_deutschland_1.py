import scraperwiki
import lxml.html
import urlparse

url = 'http://www.aktive-buergerschaft.de/buergerstiftungen/unsere_leistungen/buergerstiftungsfinder'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

for dl in root.cssselect("#content dl"):
    ldts = dl.cssselect("dt")
    ldds = dl.cssselect("dd")
    dts = [dt.text_content().encode('utf-8') for dt in ldts]
    dds = [dd.text_content().encode('utf-8') for dd in ldds]
    data = {'Name': dts[0], 'Rechtsform': dds[0], 'Ansprechpartner': dds[1][18:],'Strasse': dds[2],'Postleitzahl': dds[3][:5], 'Stadt': dds[3][6:],'Telephon': dds[4][9:],'Fax': dds[5][9:],'Email': dds[6][7:]}
    data["linkurl"] = urlparse.urljoin(url,ldds[8][0].attrib.get("href"))
    data["hompageurl"] = ldds[7][0].attrib.get("href")
    print data
    scraperwiki.sqlite.save(unique_keys=['Strasse','Postleitzahl','Stadt'], data=data)
