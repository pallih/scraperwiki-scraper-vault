import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.ebay.at/sch/i.html?scp=ce0&_sacat=See-All-Categories&_from=R40&_nkw=raspberry+pi&_pppn=r1&_rdc=1")
root = lxml.html.fromstring(html)

for t in root.cssselect("div#ResultSetItems tr"):
    link = ""
    title = ""
    price = 0.0
    for e in t.cssselect("div.ittl a"):
        link = e.attrib['href']
        title = e.text
    for e in t.cssselect("td.prc div.g-b"):
        tmp = e.text.strip(' \t\n\r').replace(",",".")
        price = float(tmp[3:])
    data = {
        'link' : link,
        'title' : title,
        'price' : price,
        'user' : "",
        'location' : "",
        'sendTo' : ""
    }
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)

for e in scraperwiki.sqlite.select("* from swdata"):
    html = scraperwiki.scrape(e['link'])
    root = lxml.html.fromstring(html)
    for td in root.cssselect("td#vieu_si span.mbg-nw"):
        e['user'] = td.text
    td = root.cssselect("td#isclmn div.sh-DlvryDtl span.g-b")
    e['location'] = td[0].text
    e['sendTo'] = td[1].text
    scraperwiki.sqlite.save(unique_keys=['link'], data=e, table_name="swdata")
