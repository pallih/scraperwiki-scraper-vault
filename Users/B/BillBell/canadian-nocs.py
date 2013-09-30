import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www5.hrsdc.gc.ca/NOC/English/NOC/2006/QuickSearch.aspx?val65=*'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

links = soup.findAll('a') 
l = 0
for link in links:
    href = None
    for attr in link . attrs :
        if attr [ 0 ] == u'href' :
            href = attr [ 1 ]
            break
    if href and 'ProfileQuickSearch.aspx' in href :
        title = None
        for attr in link . attrs :
            if attr [ 0 ] == u'title' :
                title = attr [ 1 ]
                break
#        l += 1
#        print title
#        if l > 10 :
#            break
        record = { 'NOC': title [ : 4 ], 'title': title [ 5 : ] }
        scraperwiki.sqlite.save ( [ 'NOC' ], record )
        import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www5.hrsdc.gc.ca/NOC/English/NOC/2006/QuickSearch.aspx?val65=*'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

links = soup.findAll('a') 
l = 0
for link in links:
    href = None
    for attr in link . attrs :
        if attr [ 0 ] == u'href' :
            href = attr [ 1 ]
            break
    if href and 'ProfileQuickSearch.aspx' in href :
        title = None
        for attr in link . attrs :
            if attr [ 0 ] == u'title' :
                title = attr [ 1 ]
                break
#        l += 1
#        print title
#        if l > 10 :
#            break
        record = { 'NOC': title [ : 4 ], 'title': title [ 5 : ] }
        scraperwiki.sqlite.save ( [ 'NOC' ], record )
        