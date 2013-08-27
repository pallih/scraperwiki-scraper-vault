# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

# An improved version of part of code found in 
# http://github.com/sunlightlabs/openstates/blob/master/fiftystates/scrape/fl/legislators.py
    
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

kkeys = set(['Recreation', 'Education', 'Grandchildren', 'Historical', 'Born', 'Military Service', 'Spouse', 'Children', 'Religious Affiliation', 'Occupation'])
def ParsePage(purl):
    print purl
    root = lxml.html.parse(purl).getroot()
    pdata = { }
    table = None
    for b in root.cssselect('table tr td b'):
        if b.text.strip() == 'Occupation:':
            table = b.getparent().getparent().getparent()
            break
            
    if table is not None:        
        for tr in table.cssselect('tr'):
            assert len(tr) == 2 and tr[0].tag == 'td' and tr[0][0].tag == 'b', lxml.etree.tostring(tr)
            #print lxml.etree.tostring(tr)
            v = re.sub('<.*?>|&#13;', '', lxml.etree.tostring(tr[1])).strip()
            k = tr[0][0].text.strip(' :')
            if k == 'Grandchild':
                k = 'Grandchildren'
            if k == 'Child':
                k = 'Children'
            pdata[k] = v
        assert kkeys.issuperset(pdata.keys()), pdata.keys()

    for a in root.cssselect('td.memberLeftCol div.leftcolumn a'):
        if a.get('href')[:7] == 'mailto:':
            pdata['email'] = a.get('href')[7:]

    return pdata


def Main():
    url = "http://www.flsenate.gov/Legislators/index.cfm?Tab=legislators"
    root2 = lxml.html.parse(url).getroot() #only onle html block now.
               
    title = root2.cssselect('h1')[1].text.strip()
    assert title == '2010-2012 Senators'
    
    rows = root2.cssselect('table#Senators tr')
    tr = rows[0]
    headers = (tr[0].text, tr[1][0].text, tr[2][0].text, tr[3][0].text)
    assert headers == ('Legislator', 'District', 'Party', 'County'), lxml.etree.tostring(tr)
    for tr in rows[1:]:
        assert len(tr) == 4 
        assert tr[0].tag == 'th' 
        assert tr[0][0].tag == 'a'
        lxml.etree.tostring(tr)
        values = (tr[0][0].text, tr[1].text, tr[2].text, tr[3].text)
        data = dict(zip(headers, values))
        data['url'] = urlparse.urljoin(url, tr[0][0].get('href'))
        data['title'] = title
        data['state'] = 'FL'

        pdata = ParsePage(data['url'])
        data.update(pdata)
        print scraperwiki.sqlite.show_tables()  
        scraperwiki.datastore.save(unique_keys=['title', 'District', 'Legislator'], data=data)

#ParsePage('http://www.flsenate.gov/Legislators/index.cfm?Members=View+Page&District_Num_Link=029&Submenu=1&Tab=legislators&chamber=Senate&CFID=237157675&CFTOKEN=21290235')
                          
Main()

                        

