import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/temes/heut/MSGE.htm#jetzt")
         
root = lxml.html.fromstring(html)

for trs in root.cssselect("div#main div table tbody tr"):           
    tds = trs.cssselect("td")

    if len(tds) >= 5:
            data = {
                'zeit' : tds[0].text_content(),
                'ozon' : tds[2].text_content(),
                'no' : tds[3].text_content(),
#                'no2' : tds[4].text_content(),
#                'so2' : tds[9].text_content(),
#                'pm10' : tds[10].text_content(),
            }

            #print Data
            scraperwiki.sqlite.save(unique_keys=['zeit'], data=data)
    
    
        import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.lanuv.nrw.de/luft/temes/heut/MSGE.htm#jetzt")
         
root = lxml.html.fromstring(html)

for trs in root.cssselect("div#main div table tbody tr"):           
    tds = trs.cssselect("td")

    if len(tds) >= 5:
            data = {
                'zeit' : tds[0].text_content(),
                'ozon' : tds[2].text_content(),
                'no' : tds[3].text_content(),
#                'no2' : tds[4].text_content(),
#                'so2' : tds[9].text_content(),
#                'pm10' : tds[10].text_content(),
            }

            #print Data
            scraperwiki.sqlite.save(unique_keys=['zeit'], data=data)
    
    
        