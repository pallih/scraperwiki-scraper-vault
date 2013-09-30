import scraperwiki, lxml.html

def scrape_paginated_listing(pagination):

    order = 'desc'
    sort = 'count'
    state = 'open'

    uri_base = 'http://epetitions.direct.gov.uk'
    uri = '%s/petitions?order=%s&page=%s&sort=%s&state=%s' % (uri_base, order, str(pagination), sort, state)
    html = scraperwiki.scrape(uri)
    
    root = lxml.html.fromstring(html)
    
    #table tbody tr td.name a.text_link[href] = /petitions/7337
    #table tbody tr td.name a = Convicted London rioters should loose all benefits. <span class="link_prompt">View</span>
    #table tbody tr td.sig_count = 167,751
    #table tbody tr td.closing_date = 09/02/2012
    
    data = []
    
    for tr in root.cssselect('table tbody tr'):
        
        data.append({
        'URI'               : uri_base + tr.cssselect('td.name a.text_link')[0].get('href'),
        'title'             : tr.cssselect('td.name a.text_link')[0].text_content(),
        'signature_count'   : int(tr.cssselect('td.sig_count')[0].text_content().replace(",","")),
        'closing_date'      : tr.cssselect('td.closing_date')[0].text_content()
        })
    
    scraperwiki.sqlite.save(unique_keys=['URI'], data=data)
    
    

for n in range(1,10):
    scrape_paginated_listing(n) 

import scraperwiki, lxml.html

def scrape_paginated_listing(pagination):

    order = 'desc'
    sort = 'count'
    state = 'open'

    uri_base = 'http://epetitions.direct.gov.uk'
    uri = '%s/petitions?order=%s&page=%s&sort=%s&state=%s' % (uri_base, order, str(pagination), sort, state)
    html = scraperwiki.scrape(uri)
    
    root = lxml.html.fromstring(html)
    
    #table tbody tr td.name a.text_link[href] = /petitions/7337
    #table tbody tr td.name a = Convicted London rioters should loose all benefits. <span class="link_prompt">View</span>
    #table tbody tr td.sig_count = 167,751
    #table tbody tr td.closing_date = 09/02/2012
    
    data = []
    
    for tr in root.cssselect('table tbody tr'):
        
        data.append({
        'URI'               : uri_base + tr.cssselect('td.name a.text_link')[0].get('href'),
        'title'             : tr.cssselect('td.name a.text_link')[0].text_content(),
        'signature_count'   : int(tr.cssselect('td.sig_count')[0].text_content().replace(",","")),
        'closing_date'      : tr.cssselect('td.closing_date')[0].text_content()
        })
    
    scraperwiki.sqlite.save(unique_keys=['URI'], data=data)
    
    

for n in range(1,10):
    scrape_paginated_listing(n) 

