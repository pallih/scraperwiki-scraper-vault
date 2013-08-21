import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www.saa.gov.uk/search.php?SEARCHED=1&SEARCH_TERM=ab10+1xy&DISPLAY_COUNT=100#results')
#http://news.bbc.co.uk/sport2/hi/football/eng_prem/table/default.stm

page = BeautifulSoup.BeautifulSoup(html)
print page
#find rows that contain
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: #[1:]: what does this do?
        if row.get('class','') in ['bgdarkgrey', 'bglightgrey']:
            refno = row.contents[1].string
            taxband = row.contents[5].string
            date = row.contents[7].string
            address = row.contents[0].string
            print refno,taxband,date,address
            data = {'ref':refno,
                    'taxband':taxband,
                    'date':date,
                    'address':address}
            scraperwiki.sqlite.save(unique_keys=['ref'], data=data)



