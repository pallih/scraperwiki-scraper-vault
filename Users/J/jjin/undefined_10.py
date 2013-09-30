import scraperwiki
html = scraperwiki.scrape("http://www.imdb.com/chart/top?ref_=nb_mv_3_chttp")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class= 'center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'rank' :       tds[0].text_content(),
            'rating' : tds[1].text_content(),
            'title' : (tds[2].text_content(),
            'votes' : (tds[3].text_content())
        
        }
        scraperwiki.sqlite.save(unique_keys=['votes'], data=data)import scraperwiki
html = scraperwiki.scrape("http://www.imdb.com/chart/top?ref_=nb_mv_3_chttp")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[class= 'center'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==4:
        data = {
            'rank' :       tds[0].text_content(),
            'rating' : tds[1].text_content(),
            'title' : (tds[2].text_content(),
            'votes' : (tds[3].text_content())
        
        }
        scraperwiki.sqlite.save(unique_keys=['votes'], data=data)