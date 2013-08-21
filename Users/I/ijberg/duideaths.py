import scraperwiki

html = scraperwiki.scrape("http://www.madd.org/blog/2012/december/2011-State-data.html")



import lxml.html           
root = lxml.html.fromstring(html)
mydiv = (root.cssselect("div.post"))[0]
for tr in mydiv.cssselect("tr")[2:-3]:

    print lxml.html.tostring(tr)
    tds = tr.cssselect("td")
    data = {
            'state' : tds[0].text_content(),
            'deathcount' : tds[1].text_content(), 'Pdrunkdeath' : tds[2].text_content()
        }
    scraperwiki.sqlite.save(unique_keys=['state', 'deathcount', 'Pdrunkdeath'], data=data) 

    

