import scraperwiki
import lxml.html
import string
# Blank Python

#scraperwiki.sqlite.execute("ALTER TABLE 'top 100 songs' RENAME TO swdata")

#exit()

#url = 'http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-'
part1 = 'http://www.manta.com/mb?pg='
part2 = '&refine_company_loctype=H&refine_company_rev=R10&refine_company_pubpri=private'

#result_xpath = '//table/tr'

for i in range(1,1):
    fetchurl = [ part1 + str(i) + part2]
    html = scraperwiki.scrape(fetchurl)
    scraperwiki.sqlite.save(html)
#    record = {}
#    record['i'] = i
#    root = lxml.html.fromstring(html)
#    results = root.xpath (result_xpath)
#    for h2 in results:
#            record['song'] = h2[0].text_content().strip()
#            pause(5)
#            scraperwiki.sqlite.save(unique_keys=['number', 'i'], data=record, table_name='swdata')
 
import scraperwiki
import lxml.html
import string
# Blank Python

#scraperwiki.sqlite.execute("ALTER TABLE 'top 100 songs' RENAME TO swdata")

#exit()

#url = 'http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-'
part1 = 'http://www.manta.com/mb?pg='
part2 = '&refine_company_loctype=H&refine_company_rev=R10&refine_company_pubpri=private'

#result_xpath = '//table/tr'

for i in range(1,1):
    fetchurl = [ part1 + str(i) + part2]
    html = scraperwiki.scrape(fetchurl)
    scraperwiki.sqlite.save(html)
#    record = {}
#    record['i'] = i
#    root = lxml.html.fromstring(html)
#    results = root.xpath (result_xpath)
#    for h2 in results:
#            record['song'] = h2[0].text_content().strip()
#            pause(5)
#            scraperwiki.sqlite.save(unique_keys=['number', 'i'], data=record, table_name='swdata')
 
