import scraperwiki           
html = scraperwiki.scrape("http://gruene-bonn.de/nc/kalender.html")
#print html

def get_data(divdata):
    import lxml.html as lh
    doc=lh.fromstring(html)
    for div in doc.cssselect(divdata):
        G = div.cssselect("h3")
        D = div.cssselect("div.date")
        O = div.cssselect("div.meta")
        data = {
        'Gruppe' : G[0].text_content(),
        'Datum'  : D[0].text_content(),
        'Ort'    : O[0].text_content().replace(' Ort:','')
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=['Datum'], data=data)


get_data('div.event')
get_data('div.event even')



