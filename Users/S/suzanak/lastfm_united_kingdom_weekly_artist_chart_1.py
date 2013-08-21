#extract the artist chart for the UK for the most recent completed week

#to do: use http://en.wikipedia.org/wiki/ISO_3166-1 to build a list of all countries, then get all their charts.
#       update: last.fm don't actually seem to use the list as it stands (see: Bolivia vs Bolivia, Plurinational State of)
#done!: specify that the rank is an integer for sorting purposes on scraperwiki page(?)
#done!: fix problem with unicode names being mangled
#done!: make sure that all data is dropped before the scrape runs

import scraperwiki
import lxml.html

#we just want fresh data each run, so clear out the table and define the schema
scraperwiki.sqlite.execute("drop table if exists chart")
scraperwiki.sqlite.execute("create table chart (rank INTEGER NOT NULL, artist, playcount INTEGER NOT NULL)")
scraperwiki.sqlite.commit()

#gah... i hate unicode issues! this took a good while to get working - can't see why it didn't handle this without a decode
html = scraperwiki.scrape("http://www.last.fm/place/United+Kingdom/+charts?rangetype=week&subtype=artists").decode('utf-8')
#print html

root = lxml.html.fromstring(html)
for tr in root.xpath('//*[@id="content"]/div[2]/table/tbody/tr'):
        tds = tr.cssselect("td")
        data = {
            'rank' : tds[0].text_content().strip(),
            'artist' : tds[2].cssselect("a")[0].text_content(),
            'playcount' : tds[5].cssselect("span")[0].text_content().replace(",", "")
        }
        #print data
        scraperwiki.sqlite.save(unique_keys=[], data=data, table_name="chart")


