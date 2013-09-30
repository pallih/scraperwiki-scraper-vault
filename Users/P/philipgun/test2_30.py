import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

scraperwiki.sqlite.execute("CREATE TABLE `tttt` (`test` integer, `country` text, `years_in_school` integer, `test2` integer, `test3` integer)")           
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
    



        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content()),
            'test' : int(tds[4].text_content()),
            'test2' : int(tds[4].text_content()),
            'test3' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

scraperwiki.sqlite.execute("CREATE TABLE `tttt` (`test` integer, `country` text, `years_in_school` integer, `test2` integer, `test3` integer)")           
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
    



        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content()),
            'test' : int(tds[4].text_content()),
            'test2' : int(tds[4].text_content()),
            'test3' : int(tds[4].text_content())
        }
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
