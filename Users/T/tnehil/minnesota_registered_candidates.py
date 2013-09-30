import scraperwiki
import mechanize
import csv

url = 'http://candidates.sos.state.mn.us/'

br = mechanize.Browser()
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False) # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(url)

br.select_form(nr=0)

br.set_all_readonly(False)
br['__EVENTTARGET'] ='ctl00$ContentPlaceHolder1$lbStateMediaFile'
br['__EVENTARGUMENT'] = ''

br.find_control("ctl00$ContentPlaceHolder1$btnOfficeTitle").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByOfficeLevel").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByCandidateName").disabled = True

response2 = br.submit()

scraperwiki.sqlite.execute("update swdata set dropout = 1")
scraperwiki.sqlite.commit() 

candidates = csv.reader(response2,delimiter=';', quotechar='|')
for row in candidates:
    data = {'office':row[3],'candidate':row[1].lower(),'party':row[5], 'website':row[15], 'dropout':0,'candname':row[1].lower().replace('.','').replace(' ','')}
    scraperwiki.sqlite.save(unique_keys=['candname'], data=data)

import scraperwiki
import mechanize
import csv

url = 'http://candidates.sos.state.mn.us/'

br = mechanize.Browser()
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False) # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(url)

br.select_form(nr=0)

br.set_all_readonly(False)
br['__EVENTTARGET'] ='ctl00$ContentPlaceHolder1$lbStateMediaFile'
br['__EVENTARGUMENT'] = ''

br.find_control("ctl00$ContentPlaceHolder1$btnOfficeTitle").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByOfficeLevel").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByCandidateName").disabled = True

response2 = br.submit()

scraperwiki.sqlite.execute("update swdata set dropout = 1")
scraperwiki.sqlite.commit() 

candidates = csv.reader(response2,delimiter=';', quotechar='|')
for row in candidates:
    data = {'office':row[3],'candidate':row[1].lower(),'party':row[5], 'website':row[15], 'dropout':0,'candname':row[1].lower().replace('.','').replace(' ','')}
    scraperwiki.sqlite.save(unique_keys=['candname'], data=data)

