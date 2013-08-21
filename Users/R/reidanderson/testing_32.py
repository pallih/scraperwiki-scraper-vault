import scraperwiki

# Blank Python
import lxml.html
html = scraperwiki.scrape("")
root = lxml.html.fromstring(html) 
for tr in root.cssselect("div[id='content'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==24: 
        data = {
            'rank' : tds[1].text_content(),
            'player' : tds[2].text_content(),
            'team' : tds[3].text_content(),
            'age' : tds[4].text_content(),
            'notes' : tds[5].text_content(),
            #'notes' : tds[6].text_content(),
            'average' : tds[14].text_content()
            #'years_in_school' : int(tds[4].text_content())
        }
        #print(data)
    scraperwiki.sqlite.save(unique_keys=['rank'], data=data)
