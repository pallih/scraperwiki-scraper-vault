import scraperwiki
html = scraperwiki.scrape("http://downtown.dk/kbh/deals")
print html
import lxml.html
root = lxml.html.fromstring(html)
for el4 in root.cssselect("div.text_container a"):
    data = {
    'title' : el4.text
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)
for el5 in root.cssselect("div.value span"):
    data = {
    'value' : el5.text,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['value'], data=data)
for el6 in root.cssselect("div.savings span"):
    data = {
    'save' : el6.text,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['save'], data=data)
for el in root.cssselect("div.title"):    
    data = {
    'title' : el.text
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)
for el2 in root.cssselect("div.value"):
    data = {
    'value' : el2.text,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['value'], data=data)
for el3 in root.cssselect("div.save"):
    data = {
    'save' : el3.text,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['save'], data=data)
