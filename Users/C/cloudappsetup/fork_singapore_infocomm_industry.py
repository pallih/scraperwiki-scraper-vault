# Blank Python

import scraperwiki
import lxml.html


count = 0
page = 0

while page < 400:
    html = scraperwiki.scrape("http://www.sitf.org.sg/index.php?option=com_comprofiler&task=usersList&listid=2&Itemid=30&cbsecurityg1=cbm_0fa7c0ed_77365b53_c4182bfe987268bb82b9489217c0cd9d&limitstart=%d" % page)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table[id='cbUserTable'] tr"):
        tds = tr.cssselect("td")
    
        if not tds:
            # Header row
            continue
        
        name = tds[0].text_content()
        url = tds[1].cssselect('a')[0].get('href')

        details = scraperwiki.scrape(url)
        droot = lxml.html.fromstring(details)
    
        data = {}
        data['Email'] = ''

        for row in droot.cssselect("table[class='cbFields'] tr"):
            k = row.cssselect('td')[0].text_content()
            v = row.cssselect('td')[1].text_content()
            
            if   k == 'Company Name:':
                data['Name'] = v
            elif k == 'Address 1:':
                data['Address'] = v
            elif k == 'Address 2:':
                data['Address'] = '%s\n%s' % (data.get('Address',''), v)
            elif k == 'Postal Code:':
                data['Address'] = '%s\n%s' % (data.get('Address',''), v)
            elif k == 'Phone #:':
                data['Phone'] = v
            elif k == 'Fax #:':
                data['Fax'] = v
            elif k == 'URL:':
                data['Website'] = v
            elif k == 'Company Profile:':
                data['Description'] = v
    
        scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    
        count += 1
    page += 30

print 'Total count: %d' % count


# Blank Python

import scraperwiki
import lxml.html


count = 0
page = 0

while page < 400:
    html = scraperwiki.scrape("http://www.sitf.org.sg/index.php?option=com_comprofiler&task=usersList&listid=2&Itemid=30&cbsecurityg1=cbm_0fa7c0ed_77365b53_c4182bfe987268bb82b9489217c0cd9d&limitstart=%d" % page)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table[id='cbUserTable'] tr"):
        tds = tr.cssselect("td")
    
        if not tds:
            # Header row
            continue
        
        name = tds[0].text_content()
        url = tds[1].cssselect('a')[0].get('href')

        details = scraperwiki.scrape(url)
        droot = lxml.html.fromstring(details)
    
        data = {}
        data['Email'] = ''

        for row in droot.cssselect("table[class='cbFields'] tr"):
            k = row.cssselect('td')[0].text_content()
            v = row.cssselect('td')[1].text_content()
            
            if   k == 'Company Name:':
                data['Name'] = v
            elif k == 'Address 1:':
                data['Address'] = v
            elif k == 'Address 2:':
                data['Address'] = '%s\n%s' % (data.get('Address',''), v)
            elif k == 'Postal Code:':
                data['Address'] = '%s\n%s' % (data.get('Address',''), v)
            elif k == 'Phone #:':
                data['Phone'] = v
            elif k == 'Fax #:':
                data['Fax'] = v
            elif k == 'URL:':
                data['Website'] = v
            elif k == 'Company Profile:':
                data['Description'] = v
    
        scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    
        count += 1
    page += 30

print 'Total count: %d' % count


