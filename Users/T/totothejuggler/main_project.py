import scraperwiki
import urlparse
import lxml.html
import re
import csv
import urllib2
from BeautifulSoup import BeautifulSoup


#reader = csv.reader(data.splitlines())

data = scraperwiki.scrape('https://docs.google.com/spreadsheet/ccc?key=0AgShbXiu45eFdEJBNWlzMGhlX19SX3R3c3FBZkY3LUE#gid=0')

reader = csv.reader(data.splitlines())

for row in reader: 
    print (row[0])


loop = True
for url in urls:
    base_url = url     # this will be used for next links in urlparse.urljoin  
    next_url = url     # initialize for the first loop iteration
    
    while True:

        print "Scraping next academic", next_url 
        html = scraperwiki.scrape(next_url)
        root = lxml.html.fromstring(html)

        # within the table with class "cit-table"
        # select the rows after the first TR (tr+tr, i.e. tr preceeded by another tr)
        for tr in root.cssselect("table.cit-table tr + tr"):
            tds = tr.cssselect("td")
            if len(tds)==1:
                data = {
                'Title' : tds[0].find("a").text_content(),
                'Authors' : tds[0].find('span[@class="cit-gray"]').text_content(),
                'Citations' : tds[0].text_content(),
                'Year' : tds[3].text_content(),
                }
              #  CitationsDub.append = ( tds[1].find('//a[@class="cit-dark-link"]').text_content())
                scraperwiki.sqlite.save(unique_keys = ('Title', 'Year'), data= data)

          #  Title_array.append(tds[0].find("a").text_content())

        # --------------------
        # look for a next page
        # Next or Previous links are of class "cit-dark-link"
        # use XPath starts-with() to test link text
        # see for example http://stackoverflow.com/questions/147486/xpath-query-searching-for-an-element-with-specific-text
        # you may need starts-with(normalize-space(.), 'Test') is there is leading whitespace
        # in our case it's sufficient
        nextlinks = root.xpath('//a[@class="cit-dark-link" and starts-with(., "Next")]')
        if loop and nextlinks:
            next_url = urlparse.urljoin(base_url, nextlinks[0].get('href'))
        else:
            break


        #CitationsLink = root.xpath()
print CitationsDub[0]
#print Title_array[4]

#print Title_array = list(set(Title_array))

"""
def RemoveDuplicates(iterable):
    seen = set()
    result = []
    for item in iterable:
        seen.add(item)
        results.appened(item)
    return result
"""




 
