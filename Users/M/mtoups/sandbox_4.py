from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring

def upload_data(url):
    
    muffin = scrape(url)
    
    banana = fromstring(muffin)
    
    tea = banana.cssselect('table')
    you = tea[2]
    marcus = you.cssselect('tr')
    #xpath
    
    headers = ['employer','download','location','union','local','naics','num_workes','expiration_date' ]
    
    for jay in marcus[1:10]:
        tractor = jay.cssselect('td,th') # or * gets all of them
        aidan = [apple.text_content() for apple in tractor]
        data = dict(zip(headers,aidan))
        print(data)
        #save([],data)
    print data
    
URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
upload_data(URL)

#    for apple in tractor:
#        if i == 0:
#            headers.append(apple.text_content())
#        else:
#            data
#        print apple.text_content()
#    i = i + 1

# first parameter are the list of unique columns
#data={
#    'firstname':'sean',
#    'lastname':'levine'
#}
#save([],data)

# Blank Python

#url = 'http://www.columbia.edu'
#page = fromstring(scrape(url))

#a=page.cssselect('a')[0]

#print(a.attrib['href'])

#print(sean)
from scraperwiki import scrape
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring

def upload_data(url):
    
    muffin = scrape(url)
    
    banana = fromstring(muffin)
    
    tea = banana.cssselect('table')
    you = tea[2]
    marcus = you.cssselect('tr')
    #xpath
    
    headers = ['employer','download','location','union','local','naics','num_workes','expiration_date' ]
    
    for jay in marcus[1:10]:
        tractor = jay.cssselect('td,th') # or * gets all of them
        aidan = [apple.text_content() for apple in tractor]
        data = dict(zip(headers,aidan))
        print(data)
        #save([],data)
    print data
    
URL='http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm'
upload_data(URL)

#    for apple in tractor:
#        if i == 0:
#            headers.append(apple.text_content())
#        else:
#            data
#        print apple.text_content()
#    i = i + 1

# first parameter are the list of unique columns
#data={
#    'firstname':'sean',
#    'lastname':'levine'
#}
#save([],data)

# Blank Python

#url = 'http://www.columbia.edu'
#page = fromstring(scrape(url))

#a=page.cssselect('a')[0]

#print(a.attrib['href'])

#print(sean)
