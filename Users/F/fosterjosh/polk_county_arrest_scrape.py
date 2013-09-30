from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime

def ScrapeProfile(site, link):
    page = urlopen(link)
    rawtext = page.read()
    html = fromstring(rawtext)
    print tostring(html)
    tables = html.cssselect('table') #3 tables on profile, all with valid information
    
    try:
        imgs = html.cssselect('img')
        data = {'image_link': site + imgs[1].attrib['src']}
    except IndexError:
        print "image not available"
        data = {'image_link': 'None'}
    
    divinfo = html.cssselect("#inmateAddress")
    address = str(divinfo[0].text_content().strip())
    address = address[5:].strip()
    data['address'] = address

    divinfo = html.cssselect("#holdingLocation")
    location = str(divinfo[0].text_content().strip())
    location =  location[17:]
    data['location'] = location
    

    Table_HEADERS = [['id','name','book_date'],
    ['age','height','weight','race', 'sex', 'eye', 'hair'],
    ['case_num', 'description', 'bond_amount', 'bond_type']]

    for i in range(2):
        tabledata = []
        for tr in tables[i].cssselect('tr'): #this table contains ID, NAME, BOOKDATE
            cellvalues = [td.text_content().strip() for td in tr.cssselect('td')]
            tabledata.extend(cellvalues)
        data = dict(data.items() + dict(zip(Table_HEADERS[i], tabledata)).items())    
    
    
    for tr in tables[2].cssselect('tr')[1:]: #Table 2 contains case number(s), description and cash or Bond type
        cellvalues = [td.text_content().strip() for td in tr.cssselect('td')]
        data1 = dict(zip(Table_HEADERS[2], cellvalues))
        data3 = dict((data.items() + data1.items()))
        data3['age'] = int(data3['age'])
        data3['weight'] = int(data3['weight'])
        data3['id'] = int(data3['id'])
        data3['bond_amount'] = int(data3['bond_amount'].strip('$').replace(',',''))
        data3['book_date'] = datetime.datetime.strptime(data['book_date'], '%m/%d/%Y %I:%M %p').date()
        #print data3
        data3['id_CASENUM'] = str(data3['id']) +'_' + data3['case_num'] +'_' + data3['description'][:6] #used for unique key
        print data3['id_CASENUM']
        save(['id_CASENUM'],data3)

# main page has links to separate profiles
#want to scrape information off separate profiles, not just the main page
def main():
    site ='http://www.polkcountyiowa.gov/inmatesontheweb/'
    mainpage = urlopen(site)
    rawtext = mainpage.read()
    html = fromstring(rawtext)
    
    table = html.cssselect('table')[0]
    
    for tr in table.cssselect('tr')[1:]:
        link = tr.cssselect('a')[0]
        link = site + link.attrib['href']
        print link
        ScrapeProfile(site, link)

main()from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime

def ScrapeProfile(site, link):
    page = urlopen(link)
    rawtext = page.read()
    html = fromstring(rawtext)
    print tostring(html)
    tables = html.cssselect('table') #3 tables on profile, all with valid information
    
    try:
        imgs = html.cssselect('img')
        data = {'image_link': site + imgs[1].attrib['src']}
    except IndexError:
        print "image not available"
        data = {'image_link': 'None'}
    
    divinfo = html.cssselect("#inmateAddress")
    address = str(divinfo[0].text_content().strip())
    address = address[5:].strip()
    data['address'] = address

    divinfo = html.cssselect("#holdingLocation")
    location = str(divinfo[0].text_content().strip())
    location =  location[17:]
    data['location'] = location
    

    Table_HEADERS = [['id','name','book_date'],
    ['age','height','weight','race', 'sex', 'eye', 'hair'],
    ['case_num', 'description', 'bond_amount', 'bond_type']]

    for i in range(2):
        tabledata = []
        for tr in tables[i].cssselect('tr'): #this table contains ID, NAME, BOOKDATE
            cellvalues = [td.text_content().strip() for td in tr.cssselect('td')]
            tabledata.extend(cellvalues)
        data = dict(data.items() + dict(zip(Table_HEADERS[i], tabledata)).items())    
    
    
    for tr in tables[2].cssselect('tr')[1:]: #Table 2 contains case number(s), description and cash or Bond type
        cellvalues = [td.text_content().strip() for td in tr.cssselect('td')]
        data1 = dict(zip(Table_HEADERS[2], cellvalues))
        data3 = dict((data.items() + data1.items()))
        data3['age'] = int(data3['age'])
        data3['weight'] = int(data3['weight'])
        data3['id'] = int(data3['id'])
        data3['bond_amount'] = int(data3['bond_amount'].strip('$').replace(',',''))
        data3['book_date'] = datetime.datetime.strptime(data['book_date'], '%m/%d/%Y %I:%M %p').date()
        #print data3
        data3['id_CASENUM'] = str(data3['id']) +'_' + data3['case_num'] +'_' + data3['description'][:6] #used for unique key
        print data3['id_CASENUM']
        save(['id_CASENUM'],data3)

# main page has links to separate profiles
#want to scrape information off separate profiles, not just the main page
def main():
    site ='http://www.polkcountyiowa.gov/inmatesontheweb/'
    mainpage = urlopen(site)
    rawtext = mainpage.read()
    html = fromstring(rawtext)
    
    table = html.cssselect('table')[0]
    
    for tr in table.cssselect('tr')[1:]:
        link = tr.cssselect('a')[0]
        link = site + link.attrib['href']
        print link
        ScrapeProfile(site, link)

main()