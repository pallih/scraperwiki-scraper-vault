import scraperwiki
from BeautifulSoup import BeautifulSoup

# NOC 2006
starting_url = 'http://www30.hrsdc.gc.ca/NOC/English/NOC/2006/QuickSearch.aspx?val65=*'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# Jobs
links = soup.findAll('a') 
l = 0
for link in links:
    href = None
    for attr in link.attrs :
        if attr [ 0 ] == u'href' :
            href = attr [ 1 ]
            break
    if href and 'ProfileQuickSearch.aspx' in href :
        title = link.string
        if title:
            record = { 'NOC': title [ : 4 ], 'title': title [ 10 : ] }
            scraperwiki.sqlite.save ( [ 'NOC' ], record )

# Sub groups
subgroups = soup.findAll('h5') 
for subgroup in subgroups:
    title = subgroup.string
    record = { 'NOC': title [ : 3 ], 'title': title [ 9 : ]}
    scraperwiki.sqlite.save ( [ 'NOC' ], record )
    
# Groups
groups = soup.findAll(['h3', 'h4'])
for group in groups:
    print group.name
    if 'h3' == group.name:
        code = group.string[12:].strip()
        name = None
    else:
        name = group.string

    if name:
        record = { 'NOC': code, 'title': name }
        scraperwiki.sqlite.save ( [ 'NOC' ], record )
