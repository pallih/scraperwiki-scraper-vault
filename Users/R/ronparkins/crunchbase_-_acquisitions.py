import scraperwiki       
import lxml.html           

for j in range(0,16):
    for i in range(0,100):
        if ((j*100)+i) >0:
            if ((j*100)+i) < 332:
                html = scraperwiki.scrape("http://www.crunchbase.com/acquisitions?page=" + str((j*100)+i))
                root = lxml.html.fromstring(html)
                for tr in root.cssselect("div#col2_internal tr"):
                    tds = tr.cssselect("td")
                    if len(tds)==4:
                        data = {
                            'Date' : tds[0].text_content(),
                            'Target' : tds[1].text_content(), 
                            'Acquirer' : tds[2].text_content(),
                            'Price' : tds[3].text_content(),
                        }
                    scraperwiki.sqlite.save(unique_keys=['Date','Target','Acquirer','Price'], data=data)