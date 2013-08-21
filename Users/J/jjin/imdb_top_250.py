import scraperwiki
html = scraperwiki.scrape("http://www.imdb.com/chart/top?ref_=nb_mv_3_chttp")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class= 'center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==3:
        data = {
            'rank' :       tds[0].text_content(),
            'rating' : tds[1].text_content(),
            'title' : (tds[2].text_content())
        
        }
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)