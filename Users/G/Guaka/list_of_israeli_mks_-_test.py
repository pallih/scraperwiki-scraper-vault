# Scrape data from members of Knesset

# Just came across scraperwiki and I thought it was fun to try out.
# I saw the request to scrape Israeli MKs at http://scraperwiki.com/market/view/55/ and decided to start with that


import scraperwiki
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.knesset.gov.il/mk/eng/'
starting_url = base_url + 'mkindex_current_eng.asp?view=0'

def scrape_mkpage(href):
    """Scrape MK page"""
    result = { 
        'Date of Birth': None,
        'Place of Birth': None,
        'Residence': None,
        'Family Status': None,
        'Number of Children': None,
        
        'Telephone': None,
        'Fax': None,
        'Email': None,
        
        # 'Languages': None,                

        'Parliamentary Groups': None, 
    }
    mkpage = scraperwiki.scrape(href)
    mksoup = BeautifulSoup(mkpage)
    # The page is built up from JavaScript!
    gooddata = mksoup.findAll('script')
    # Take 3rd <script>
    d = gooddata[2].text.replace("\r\n", "\n") 
    # Remove some JS stuff
    d = d.replace(' sBuf += "', '')    
    d = d.replace(' sbuf += "', '')    
    d = d.replace('";' + "\n", '')

    # Scrape tabled stuff
    for thing in d.split('"EngData">')[1:]:
        dsc = thing.split(':<')[0]
        if result.has_key(dsc):
            valsoup = BeautifulSoup(thing)
            val = valsoup.findAll('td', {'class': 'EngDataText'})
            if val and dsc[0] != '<':
                result[dsc] = val[0].text
    # TODO:
    # tab 1, Particulars: Education, Profession and Languages
    # tab 2, Knesset Activities: Terms, Committees, Lobbies
    # tab 3, Public Activities
    for thing in d.split('"Title2">')[1:]:
        thing = thing.replace('<br>', '')
        dsc = thing.split('<')[0]
        print dsc
        if result.has_key(dsc):
            valsoup = BeautifulSoup(thing)
            val = valsoup.findAll('td', {'class': 'EngDataText2'})
            if val:
                result[dsc] = val[0].text
        print thing


    return result

html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)
elements = soup.findAll('a', {'class': 'EngDataText'}) 
for element in elements:
    print element.text
    href = base_url + element['href']
    record = scrape_mkpage(href)
    record['name'] = element.text
    print record
    # TODO: Data tab looks good, but scraper output is still HTML garble?
    scraperwiki.datastore.save(['name'], record) 
    # Scrape data from members of Knesset

# Just came across scraperwiki and I thought it was fun to try out.
# I saw the request to scrape Israeli MKs at http://scraperwiki.com/market/view/55/ and decided to start with that


import scraperwiki
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.knesset.gov.il/mk/eng/'
starting_url = base_url + 'mkindex_current_eng.asp?view=0'

def scrape_mkpage(href):
    """Scrape MK page"""
    result = { 
        'Date of Birth': None,
        'Place of Birth': None,
        'Residence': None,
        'Family Status': None,
        'Number of Children': None,
        
        'Telephone': None,
        'Fax': None,
        'Email': None,
        
        # 'Languages': None,                

        'Parliamentary Groups': None, 
    }
    mkpage = scraperwiki.scrape(href)
    mksoup = BeautifulSoup(mkpage)
    # The page is built up from JavaScript!
    gooddata = mksoup.findAll('script')
    # Take 3rd <script>
    d = gooddata[2].text.replace("\r\n", "\n") 
    # Remove some JS stuff
    d = d.replace(' sBuf += "', '')    
    d = d.replace(' sbuf += "', '')    
    d = d.replace('";' + "\n", '')

    # Scrape tabled stuff
    for thing in d.split('"EngData">')[1:]:
        dsc = thing.split(':<')[0]
        if result.has_key(dsc):
            valsoup = BeautifulSoup(thing)
            val = valsoup.findAll('td', {'class': 'EngDataText'})
            if val and dsc[0] != '<':
                result[dsc] = val[0].text
    # TODO:
    # tab 1, Particulars: Education, Profession and Languages
    # tab 2, Knesset Activities: Terms, Committees, Lobbies
    # tab 3, Public Activities
    for thing in d.split('"Title2">')[1:]:
        thing = thing.replace('<br>', '')
        dsc = thing.split('<')[0]
        print dsc
        if result.has_key(dsc):
            valsoup = BeautifulSoup(thing)
            val = valsoup.findAll('td', {'class': 'EngDataText2'})
            if val:
                result[dsc] = val[0].text
        print thing


    return result

html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)
elements = soup.findAll('a', {'class': 'EngDataText'}) 
for element in elements:
    print element.text
    href = base_url + element['href']
    record = scrape_mkpage(href)
    record['name'] = element.text
    print record
    # TODO: Data tab looks good, but scraper output is still HTML garble?
    scraperwiki.datastore.save(['name'], record) 
    