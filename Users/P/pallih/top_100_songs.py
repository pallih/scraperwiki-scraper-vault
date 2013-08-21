import scraperwiki
import lxml.html
import string
# Blank Python

#scraperwiki.sqlite.execute("ALTER TABLE 'top 100 songs' RENAME TO swdata")

#exit()

url = 'http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-'

result_xpath = '//table/tr'

for year in range(2008,2010):
    fetchurl = url+str(year)+'.html'
    html = scraperwiki.scrape(fetchurl)
    record = {}
    record['year'] = year
    root = lxml.html.fromstring(html)
    results = root.xpath (result_xpath)
    for tr in results:
        if year != 2011:
            record['song'] = tr[1].text_content().strip()
            record['number'] = tr[0].text_content().strip()
            record['artist'] = tr[2].text_content().strip()
            scraperwiki.sqlite.save(unique_keys=['number', 'year'], data=record, table_name='swdata')
        else:
            record['artist'] = tr[1].text_content().strip()
            record['number'] = tr[0].text_content().strip()
            record['song'] = tr[2].text_content().strip()
            print record
            scraperwiki.sqlite.save(unique_keys=['number', 'year'], data=record, table_name='swdata')

