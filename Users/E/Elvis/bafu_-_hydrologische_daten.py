import scraperwiki

# Blank Python

import lxml.html
gewaesserliste = {
    'http://www.hydrodaten.admin.ch/de/2063.html',
    'http://www.hydrodaten.admin.ch/de/2434.html',
    'http://www.hydrodaten.admin.ch/de/2016.html',
    'http://www.hydrodaten.admin.ch/de/2450.html'
}

for stationsdaten in gewaesserliste:
    html = scraperwiki.scrape(stationsdaten)
    root = lxml.html.fromstring(html)

# messwerte = root.cssselect("div#actualDataTableDiv")[0]
# print lxml.html.tostring(messwerte)

    gewaesser = root.cssselect("h1.webTitle")[0]
    sampledate = root.cssselect("span.LastSampleDateLabel")[0]
    abfluss = root.cssselect("td.ActualDataTableBody")[0]
    wasserstand = root.cssselect("td.ActualDataTableBody")[1]

    print gewaesser.text
    print sampledate.text
    print abfluss.text
    print wasserstand.text
    data = {
        'Gewaesser' : gewaesser.text,
        'Timestamp' : sampledate.text,
        'Abfluss' : abfluss.text,
        'Wasserstand' : wasserstand.text
    }
    scraperwiki.sqlite.save(unique_keys=['Gewaesser', 'Timestamp'], data=data)