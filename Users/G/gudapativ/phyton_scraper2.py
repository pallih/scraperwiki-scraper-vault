import scraperwiki
import lxml.html
import string

# Blank Python
html=scraperwiki.scrape("http://www.air-mandalay.com/time_winter2012.html")
#print html
root=lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    data=tr.cssselect("td")
    if len(data)==4 :          
        da={data[0].text_content().strip(),data[1].text_content().strip(),data[2].text_content().strip(),data[3].text_content().strip()}
        print da
