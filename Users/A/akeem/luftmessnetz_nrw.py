import scraperwiki
import lxml.html

#definiere Datenquelle (url)
html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/immissionen/aktluftqual/eu_pm10_akt.htm")
root = lxml.html.fromstring(html)

time = root.cssselect("h2")[0].text_content()
print time

for tr in root.cssselect("tr")[2:]:
    tds = tr.cssselect("td")
    data = {
      'time': time,
      'station' : tds[0].text_content(),
      'kuerzel' : tds[1].text_content(),
      'TW-1' : tds[2].text_content(),
      'TW' : tds[3].text_content(),
      'Wert' : tds[4].text_content(),
}

    print data
        

    scraperwiki.sqlite.save(unique_keys=["kuerzel","time"], data=data)
