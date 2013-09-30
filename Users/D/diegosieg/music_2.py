import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.last.fm/place/Brazil/+charts?rangetype=week&subtype=artists")

root = lxml.html.fromstring(html)
for tr in root.xpath('//*[@id="content"]/div[2]/table/tbody/tr'):
        tds = tr.cssselect("td")
        data = {
            'rank' : tds[0].text_content().strip(),
            'artist' : tds[2].cssselect("a")[0].text_content(),
            'playcount' : tds[5].cssselect("span")[0].text_content().replace(",", "")
        }
        print data
        scraperwiki.sqlite.save(unique_keys=[], data=data)



import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.last.fm/place/Brazil/+charts?rangetype=week&subtype=artists")

root = lxml.html.fromstring(html)
for tr in root.xpath('//*[@id="content"]/div[2]/table/tbody/tr'):
        tds = tr.cssselect("td")
        data = {
            'rank' : tds[0].text_content().strip(),
            'artist' : tds[2].cssselect("a")[0].text_content(),
            'playcount' : tds[5].cssselect("span")[0].text_content().replace(",", "")
        }
        print data
        scraperwiki.sqlite.save(unique_keys=[], data=data)



