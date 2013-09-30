import scraperwiki
import lxml.html

k = 0
while k > -1:

# 1. Eine HTML-Seite aus dem Web laden.
    if k == 0:
        html = scraperwiki.scrape("http://www.zitty.de/list?type=address&category[categories]=Galerien")
    else:
        html = scraperwiki.scrape("http://www.zitty.de/list?type=address&category[categories]=Galerien&page=" + str(k))

# 2. Die HTML-Seite in eine bearbeitbare XML-Struktur aufsplitten (parsen)
    root = lxml.html.fromstring(html)


# 3. Aus dem XML die benötigten Daten auslesen und weiter bearbeiten
    from lxml.cssselect import CSSSelector
    linkselector = CSSSelector("a")

    for th in root.cssselect("th.teaser-cell"):
        for e in linkselector(th): innerhtml = "http://www.zitty.de/" + e.get('href').strip()
        leaf = lxml.html.fromstring(scraperwiki.scrape(innerhtml))

        data = {}
        keys = []
        for dt in leaf.cssselect("dt"): keys.append(dt.text_content())

        i = 0
        for dd in leaf.cssselect("dd"):
            if keys[i] == "Anschrift":
                addr = dd.cssselect("li")
                data.update( { "name" : addr[0].text_content(), "address" : addr[1].text_content(), "district" : addr[2].text_content() } )
        #elif weitere Daten wie Kontakt und Web hinzufügbar
            i += 1

        for latitude in leaf.cssselect("span.latitude"): data.update( {"latitude" : latitude.text_content().strip()} )
        for longitude in leaf.cssselect("span.longitude"): data.update( {"longitude" : longitude.text_content().strip()} )

    # 4. Daten speichern
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)

    k += 10

import scraperwiki
import lxml.html

k = 0
while k > -1:

# 1. Eine HTML-Seite aus dem Web laden.
    if k == 0:
        html = scraperwiki.scrape("http://www.zitty.de/list?type=address&category[categories]=Galerien")
    else:
        html = scraperwiki.scrape("http://www.zitty.de/list?type=address&category[categories]=Galerien&page=" + str(k))

# 2. Die HTML-Seite in eine bearbeitbare XML-Struktur aufsplitten (parsen)
    root = lxml.html.fromstring(html)


# 3. Aus dem XML die benötigten Daten auslesen und weiter bearbeiten
    from lxml.cssselect import CSSSelector
    linkselector = CSSSelector("a")

    for th in root.cssselect("th.teaser-cell"):
        for e in linkselector(th): innerhtml = "http://www.zitty.de/" + e.get('href').strip()
        leaf = lxml.html.fromstring(scraperwiki.scrape(innerhtml))

        data = {}
        keys = []
        for dt in leaf.cssselect("dt"): keys.append(dt.text_content())

        i = 0
        for dd in leaf.cssselect("dd"):
            if keys[i] == "Anschrift":
                addr = dd.cssselect("li")
                data.update( { "name" : addr[0].text_content(), "address" : addr[1].text_content(), "district" : addr[2].text_content() } )
        #elif weitere Daten wie Kontakt und Web hinzufügbar
            i += 1

        for latitude in leaf.cssselect("span.latitude"): data.update( {"latitude" : latitude.text_content().strip()} )
        for longitude in leaf.cssselect("span.longitude"): data.update( {"longitude" : longitude.text_content().strip()} )

    # 4. Daten speichern
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)

    k += 10

