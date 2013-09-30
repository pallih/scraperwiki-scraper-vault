import scraperwiki

import lxml.html

html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")

root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        #print data,we could print into tha console
        #div,td=CSS selectors
        #Here we use them to select all the table rows. And then, for each of those rows,
        #we select the individual cells, and if there are 12 of them (ie: we are in the main
        #table body, rather than in one of the header rows), we extract the country name and schooling statistic.
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
        #the line must be inteneded with spaces/tabs(this is a hell of a problem)
#goto your scrapers,click explore with api use the query,click run,get JSON object

#select * from swdata order by years_in_school desc limit 10

#the records for the ten countries where children spend the most years at school.