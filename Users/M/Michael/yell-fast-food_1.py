import scraperwiki
import urlparse
import lxml.html

html = scraperwiki.scrape("http://www.localmole.co.uk/find-business/Birmingham/Takeaways/?page=1")
print html

root = lxml.html.fromstring(html)
for div in root.cssselect("div.search-result"):
    td1 = div.cssselect("h3")
    td2 = div.cssselect("p.address")
    td3 = div.cssselect("p.tel")
    data = {
        'name' : td1[0].text_content(),
        'address' : td2[0].text_content(),
        'tel' : td3[0].text_content()
    }
    print data

    ## Replace 'print data' with this to import to datastore
    # scraperwiki.sqlite.save(unique_keys=['name'], data=data)
import scraperwiki
import urlparse
import lxml.html

html = scraperwiki.scrape("http://www.localmole.co.uk/find-business/Birmingham/Takeaways/?page=1")
print html

root = lxml.html.fromstring(html)
for div in root.cssselect("div.search-result"):
    td1 = div.cssselect("h3")
    td2 = div.cssselect("p.address")
    td3 = div.cssselect("p.tel")
    data = {
        'name' : td1[0].text_content(),
        'address' : td2[0].text_content(),
        'tel' : td3[0].text_content()
    }
    print data

    ## Replace 'print data' with this to import to datastore
    # scraperwiki.sqlite.save(unique_keys=['name'], data=data)
