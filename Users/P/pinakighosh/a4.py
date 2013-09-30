import scraperwiki
import lxml.html

response=scraperwiki.scrape('http://envfor.nic.in/fsi/sfr99/chap3/arunachal/arunachal.html#fr')
root=lxml.html.fromstring(response)
for el in root.cssselect("table tr"):
    for el2 in el.cssselect("td div"):
        text=el2.text_content().replace('\n','').replace('\r','')
        print text
import scraperwiki
import lxml.html

response=scraperwiki.scrape('http://envfor.nic.in/fsi/sfr99/chap3/arunachal/arunachal.html#fr')
root=lxml.html.fromstring(response)
for el in root.cssselect("table tr"):
    for el2 in el.cssselect("td div"):
        text=el2.text_content().replace('\n','').replace('\r','')
        print text
