import scraperwiki

# Blank Python
print "Hello, coding in the cloud!"
import lxml.html

html = scraperwiki.scrape("http://www.cookcountysheriff.org/crimeblotter/crimeblotter_Skokie.html")
root = lxml.html.fromstring(html)
data_id = 1
for tr in root.cssselect("div[class='AccordionPanelContent'] tr"):
    #print "Loop"
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'date_time' : tds[0].text_content(),
            'location' : tds[1].text_content(),
            'incident' : tds[2].text_content(),
            'my_id'  : data_id
        }
        scraperwiki.sqlite.save(unique_keys=['my_id'], data=data)
        data_id = data_id + 1
print "done"
