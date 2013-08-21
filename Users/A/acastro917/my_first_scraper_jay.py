import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://zigsa.com/demo/table/")

print html


root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
        'flight_num' : tds[0].text_content(),
        'destination' : tds[2].text_content(),
        'date' : tds[4].text_content(),
        'airline' : tds[8].text_content(),
        'time' : tds[5].text_content(),
        'remarks' : tds[3].text_content(),
        'flight_type' : tds[7].text_content(),



       
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['flight_num'], data=data)

