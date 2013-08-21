# -*- coding: utf-8 -*-
import mechanize
url = "http://www.mym.co.uk/index.cfm?fuseAction=CTM.companyList&categoryID=4"
dechrau_url="http://www.mym.co.uk/"


br=mechanize.Browser()
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

r = br.open(url)
html = r.read()
data = {}
import re
p=re.compile('[\\r]+|[\\n]+|[\\t]+|\\&nbsp;')
#Oherwydd problem encodio o to:
p_cod=re.compile('C[\w\W\s\S]*Post')
p_ffon=re.compile('Rhif Ff[\w\W\s\S]*n')

import scraperwiki
#import scraperwiki.metadata
from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(html)
#print soup
for tag in soup.findAll('a',href=re.compile('[w\.\?\=\&\-\w\d]*.categoryID=4$')):
    data={}
    url_cylch=tag["href"]
    url_llawn = dechrau_url+url_cylch
    r = br.open(url_llawn)
    html = r.read()
    soup_cylch = BeautifulSoup(html)
    data['Enw'] = p.sub('',soup_cylch.find("td",{"class":"td2"}).next).decode('latin-1').encode('utf-8')
    #print data['Enw']
    data['Cyfeiriad 1'] = p.sub('',soup_cylch.find(text="Cyfeiriad:&nbsp;").findNext("td",{"class":"td2"}).contents[0])
    try:
        data['Cyfeiriad 2'] = p.sub('',soup_cylch.find(text="Cyfeiriad:&nbsp;").findNext("td",{"class":"td2"}).contents[2]).decode('latin-1').encode('utf-8')
    except:
        data['Cyfeiriad 2'] = None
        print "Cyf 2 ar goll", data
    try:
        data['Cyfeiriad 3'] = p.sub('',soup_cylch.find(text="Cyfeiriad:&nbsp;").findNext("td",{"class":"td2"}).contents[4]).decode('latin-1').encode('utf-8')
    except:
        data['Cyfeiriad 3'] = None
        print "Cyf 3 ar goll", data
    try:
        data['Cyfeiriad 4'] = p.sub('',soup_cylch.find(text="Cyfeiriad:&nbsp;").findNext("td",{"class":"td2"}).contents[6]).decode('latin-1').encode('utf-8')    
    except:
        data['Cyfeiriad 4'] = None
        print "Cyf 4 ar goll", data
    try:
        data['Cod Post'] = p.sub('',soup_cylch.find(text=p_cod).findNext("td",{"class":"td2"}).next)
    except:
        data['Cod Post'] = None
        print "Cod Post ar goll",data
    try:
        data['Rhif Ffon'] = p.sub('',soup_cylch.find(text=p_ffon).findNext("td",{"class":"td2"}).next)
    except:
        data['Rhif Ffon'] = None
        print "Rhif Ffon ar goll",data
    try:
        data['Math o gylch'] = p.sub('',soup_cylch.find(text="Math o gylch:&nbsp;").findNext("td",{"class":"td2"}).next).decode('latin-1').encode('utf-8')
    except:
        data['Math o gylch'] = None
        print "Math o gylch ar goll",data
    try:        
        latlong=scraperwiki.geo.gb_postcode_to_latlng(data['Cod Post'])
        data['latlong'] = latlong
        #print latlong
        #latlong = (1234,56789)
    except:
        latlong = None
    
    #print data
    scraperwiki.sqlite.save(['Enw'],data=data) #datastore.save(['Enw'],data=data,latlng=latlong)
    continue

#scraperwiki.metadata.save('data_columns', ['Enw', 'Math o gylch', 'Cyfeiriad 1', 'Cyfeiriad 2',
#                                           'Cyfeiriad 3','Cyfeiriad 4','Cod Post','Rhif Ffon'])
    
