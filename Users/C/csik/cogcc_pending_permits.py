import urllib,urllib2
from BeautifulSoup import BeautifulSoup
import scraperwiki

scraperwiki.metadata.save('data_columns',  ['Received',
                                            'Posted',
                                            'Operator name',
                                            'Operator number',
                                            'Employee name',
                                            'Phone',
                                            'Status',
                                            'Status url',
                                            'Status date',
                                            'Permit type',
                                            'Well name',
                                            'Well number',
                                            'Objective formation',
                                            'Proposed TD',
                                            'Facility coordinates',
                                            'Corrected coordinates',
                                            'Field',
                                            'County',
                                            ])
                                            
url = 'http://cogcc.state.co.us/COGIS/DrillingPermitsList.cfm'

values= {
            'listtype':'Pending',
            'county':'All',
            'B1':'Go%21'
         }

fields_pending = [
                    ['Received',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",0],
                    ['Posted',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",0],
                    ['Operator name',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",1],
                    ['Operator number',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",1],
                    ['Employee name',"i.contents[0].strip().replace('&nbsp;', ' ')",2],
                    ['Phone',"i.contents[0].strip().replace('&nbsp;', ' ')",3],
                    ['Status',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",4],
                    ['Status url',"i.findAll(text=True)[2].strip().replace('&nbsp;', ' ')",4],
                    ['Status date',"i.contents[0].strip().replace('&nbsp;', ' ')",5],
                    ['Permit type',"i.contents[0].strip().replace('&nbsp;', ' ')",6],
                    ['Well name',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",7],
                    ['Well number',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",7],
                    ['Objective formation',"i.contents[0].strip().replace('&nbsp;', ' ')",8],
                    ['Proposed TD',"i.contents[0].strip().replace('&nbsp;', ' ').replace(',', '')",9],
                    ['Facility coordinates',"i.contents[1].get('href')[i.contents[1].get('href').find('n=')+2:i.contents[1].get('href').find('&Sca')]+','+i.contents[1].get('href')[i.contents[1].get('href').find('t=')+2:i.contents[1].get('href').find('&Lon')]",10],
                    ['Corrected coordinates',"i.contents[1].get('href')[i.contents[1].get('href').find('t=')+2:i.contents[1].get('href').find('&Lon')]+','+i.contents[1].get('href')[i.contents[1].get('href').find('n=')+2:i.contents[1].get('href').find('&Sca')]",10],
                    ['Field',"i.contents[0].strip().replace('&nbsp;', ' ')",11],
                    ['County',"i.contents[0].strip().replace('&nbsp;', ' ')",12],
                    ['County',"i.contents[0].strip().replace('&nbsp;', ' ')",13],
]


def html_post(url, values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    html=response.read()
    return html

def html_get(url):
    response = urllib2.urlopen(url)
    html=response.read()
    return html




# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table" , { "width" : "75%" })
    rows = data_table.findAll("tr")[1:] #remove labels from row
    field_index = 0
    inc_count = 0
    for row in rows:
        # Set up our data record - we'll need it later
        permit = {}
        table_cells = row.findAll("font")
        if table_cells: 
            for scrape in fields_pending:
                i = table_cells[scrape[2]]
                #print i
                #print "trying to put " + eval(scrape[1]) + "into" + scrape[0]
                try:
                    if str(i.contents[0]) != '<br />':
                        permit[scrape[0]]=eval(scrape[1]).strip()
                        #print permit[scrape[0]]
                        #print table_cells[1].contents[2].strip()
                    else:
                        permit[scrape[0]] = "DATA MISSING"
                except IndexError, e:
                    permit[scrape[0]] = "DATA MISSING"
                    print "EXCEPTION!!!!:",e
                field_index+=1
                #print permit
        if permit.has_key('Status url') and permit.has_key('Corrected coordinates'):
            scraperwiki.datastore.save(['Status url'],permit,latlng=(eval(permit['Corrected coordinates'])))
            inc_count+=1
            #print permit
        if inc_count % 10 == 0: print "Pulling row: %d" % inc_count 
        #print "__________________________________________________"

        
html = html_post(url, values)
print len(html)
soup = BeautifulSoup(html)
scrape_table(soup)      import urllib,urllib2
from BeautifulSoup import BeautifulSoup
import scraperwiki

scraperwiki.metadata.save('data_columns',  ['Received',
                                            'Posted',
                                            'Operator name',
                                            'Operator number',
                                            'Employee name',
                                            'Phone',
                                            'Status',
                                            'Status url',
                                            'Status date',
                                            'Permit type',
                                            'Well name',
                                            'Well number',
                                            'Objective formation',
                                            'Proposed TD',
                                            'Facility coordinates',
                                            'Corrected coordinates',
                                            'Field',
                                            'County',
                                            ])
                                            
url = 'http://cogcc.state.co.us/COGIS/DrillingPermitsList.cfm'

values= {
            'listtype':'Pending',
            'county':'All',
            'B1':'Go%21'
         }

fields_pending = [
                    ['Received',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",0],
                    ['Posted',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",0],
                    ['Operator name',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",1],
                    ['Operator number',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",1],
                    ['Employee name',"i.contents[0].strip().replace('&nbsp;', ' ')",2],
                    ['Phone',"i.contents[0].strip().replace('&nbsp;', ' ')",3],
                    ['Status',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",4],
                    ['Status url',"i.findAll(text=True)[2].strip().replace('&nbsp;', ' ')",4],
                    ['Status date',"i.contents[0].strip().replace('&nbsp;', ' ')",5],
                    ['Permit type',"i.contents[0].strip().replace('&nbsp;', ' ')",6],
                    ['Well name',"i.findAll(text=True)[0].strip().replace('&nbsp;', ' ')",7],
                    ['Well number',"i.findAll(text=True)[1].strip().replace('&nbsp;', ' ')",7],
                    ['Objective formation',"i.contents[0].strip().replace('&nbsp;', ' ')",8],
                    ['Proposed TD',"i.contents[0].strip().replace('&nbsp;', ' ').replace(',', '')",9],
                    ['Facility coordinates',"i.contents[1].get('href')[i.contents[1].get('href').find('n=')+2:i.contents[1].get('href').find('&Sca')]+','+i.contents[1].get('href')[i.contents[1].get('href').find('t=')+2:i.contents[1].get('href').find('&Lon')]",10],
                    ['Corrected coordinates',"i.contents[1].get('href')[i.contents[1].get('href').find('t=')+2:i.contents[1].get('href').find('&Lon')]+','+i.contents[1].get('href')[i.contents[1].get('href').find('n=')+2:i.contents[1].get('href').find('&Sca')]",10],
                    ['Field',"i.contents[0].strip().replace('&nbsp;', ' ')",11],
                    ['County',"i.contents[0].strip().replace('&nbsp;', ' ')",12],
                    ['County',"i.contents[0].strip().replace('&nbsp;', ' ')",13],
]


def html_post(url, values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    html=response.read()
    return html

def html_get(url):
    response = urllib2.urlopen(url)
    html=response.read()
    return html




# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup):
    data_table = soup.find("table" , { "width" : "75%" })
    rows = data_table.findAll("tr")[1:] #remove labels from row
    field_index = 0
    inc_count = 0
    for row in rows:
        # Set up our data record - we'll need it later
        permit = {}
        table_cells = row.findAll("font")
        if table_cells: 
            for scrape in fields_pending:
                i = table_cells[scrape[2]]
                #print i
                #print "trying to put " + eval(scrape[1]) + "into" + scrape[0]
                try:
                    if str(i.contents[0]) != '<br />':
                        permit[scrape[0]]=eval(scrape[1]).strip()
                        #print permit[scrape[0]]
                        #print table_cells[1].contents[2].strip()
                    else:
                        permit[scrape[0]] = "DATA MISSING"
                except IndexError, e:
                    permit[scrape[0]] = "DATA MISSING"
                    print "EXCEPTION!!!!:",e
                field_index+=1
                #print permit
        if permit.has_key('Status url') and permit.has_key('Corrected coordinates'):
            scraperwiki.datastore.save(['Status url'],permit,latlng=(eval(permit['Corrected coordinates'])))
            inc_count+=1
            #print permit
        if inc_count % 10 == 0: print "Pulling row: %d" % inc_count 
        #print "__________________________________________________"

        
html = html_post(url, values)
print len(html)
soup = BeautifulSoup(html)
scrape_table(soup)      