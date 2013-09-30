import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11010'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11011'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)

starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11012'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11013'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 

starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11014'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)
        
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11015'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
    import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11010'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11011'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)

starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11012'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11013'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 

starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11014'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record)
        
starting_url = 'https://www.eura2007.fi/rrtiepa/projekti.php?projektikoodi=S11015'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('p') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.sqlite.save(["td"], record) 
    
    