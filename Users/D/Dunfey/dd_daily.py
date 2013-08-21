import scraperwiki

# Blank Python
import scraperwiki           
import lxml.html
import urllib

webquery = "http://www.digitallook.com/dlmedia/investing/uk_shares/director_dealings"

html = scraperwiki.scrape(webquery)
root = lxml.html.fromstring(html)

# table tr

tradetype = "sell"

for tr in root.cssselect("table tr"):
    ths = tr.cssselect("th")
    if len(ths)==6:
        if tradetype == "buy":
            tradetype = "sell"
        elif tradetype == "sell":
            tradetype = "buy"

    tds = tr.cssselect("td")
    if len(tds)>3:
        data = {
            'date' : tds[0].text_content(),
            'company_name' : tds[1].text_content(),
            'company_ticker' : tds[2].text_content(),
            'director' : tds[3].text_content(),
            'volume_price' : tds[4].text_content(),
            'trade_value' : tds[5].text_content(),
            'trade' : tradetype
        }
        print data
        try:
            scraperwiki.sqlite.save(unique_keys=['date','director','trade_value','trade'], data=data)
        except ValueError:
            print "opps"

