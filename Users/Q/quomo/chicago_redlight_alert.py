import scraperwiki
import lxml.html
import mechanize
import datetime
from pytz import timezone

'''
Parametersapplication/x-www-form-urlencoded
SubmitButton:Search By Plate
licenseNumber:cfk1124
licenseState:MI
ownerLastName:gordon
plateType:PAS
verb:retrieveTicketsByLP
'''

headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

base_url = 'https://parkingtickets.cityofchicago.org/CPSWeb/web/SearchTickets.jsp'
plate = 'CFK1124'
lastname = 'GORDON'
state = 'MI'
plate = 'PAS'
hiddenVal = 'retrieveTicketsByLP'

br = mechanize.Browser()
br.addheaders = headers

br.open(base_url)

br.select_form(nr=0)

#print type(br.form['licenseState'])

#br.form['SubmitButton'] = 'Search By Plate'
br.form['licenseNumber'] = plate
br.form['licenseState'] =  [state,] #the type here is a list, bc it is a dropdown
br.form['ownerLastName'] = lastname
br.form['plateType'] = [plate,] #same as state
#br.form['verb'] = hiddenVal

#req = br.submit()

req = br.click(type="submit", nr=0)
res = br.open(req)


dom = lxml.html.fromstring(res.read())

getText = dom.cssselect('font')

answers = []

for x in getText:

    for z in x:
        answers.append(z.text)


answer = answers[0] #this is the result from the site.



if answer.startswith('No Search Results'):
    answer = 'No tickets today'
else:
    answer = 'Check the site, you got a ticket'

now = datetime.datetime.now(timezone('US/Central'))

today = now.strftime("%Y-%m-%d %H:%M:%S")

myData = []

myData.append({
            "date" : today,
            "answer" : answer
        
        })    
        


scraperwiki.sqlite.save(unique_keys=["date"], data=myData, table_name="ticketlog")
import scraperwiki
import lxml.html
import mechanize
import datetime
from pytz import timezone

'''
Parametersapplication/x-www-form-urlencoded
SubmitButton:Search By Plate
licenseNumber:cfk1124
licenseState:MI
ownerLastName:gordon
plateType:PAS
verb:retrieveTicketsByLP
'''

headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

base_url = 'https://parkingtickets.cityofchicago.org/CPSWeb/web/SearchTickets.jsp'
plate = 'CFK1124'
lastname = 'GORDON'
state = 'MI'
plate = 'PAS'
hiddenVal = 'retrieveTicketsByLP'

br = mechanize.Browser()
br.addheaders = headers

br.open(base_url)

br.select_form(nr=0)

#print type(br.form['licenseState'])

#br.form['SubmitButton'] = 'Search By Plate'
br.form['licenseNumber'] = plate
br.form['licenseState'] =  [state,] #the type here is a list, bc it is a dropdown
br.form['ownerLastName'] = lastname
br.form['plateType'] = [plate,] #same as state
#br.form['verb'] = hiddenVal

#req = br.submit()

req = br.click(type="submit", nr=0)
res = br.open(req)


dom = lxml.html.fromstring(res.read())

getText = dom.cssselect('font')

answers = []

for x in getText:

    for z in x:
        answers.append(z.text)


answer = answers[0] #this is the result from the site.



if answer.startswith('No Search Results'):
    answer = 'No tickets today'
else:
    answer = 'Check the site, you got a ticket'

now = datetime.datetime.now(timezone('US/Central'))

today = now.strftime("%Y-%m-%d %H:%M:%S")

myData = []

myData.append({
            "date" : today,
            "answer" : answer
        
        })    
        


scraperwiki.sqlite.save(unique_keys=["date"], data=myData, table_name="ticketlog")
import scraperwiki
import lxml.html
import mechanize
import datetime
from pytz import timezone

'''
Parametersapplication/x-www-form-urlencoded
SubmitButton:Search By Plate
licenseNumber:cfk1124
licenseState:MI
ownerLastName:gordon
plateType:PAS
verb:retrieveTicketsByLP
'''

headers = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

base_url = 'https://parkingtickets.cityofchicago.org/CPSWeb/web/SearchTickets.jsp'
plate = 'CFK1124'
lastname = 'GORDON'
state = 'MI'
plate = 'PAS'
hiddenVal = 'retrieveTicketsByLP'

br = mechanize.Browser()
br.addheaders = headers

br.open(base_url)

br.select_form(nr=0)

#print type(br.form['licenseState'])

#br.form['SubmitButton'] = 'Search By Plate'
br.form['licenseNumber'] = plate
br.form['licenseState'] =  [state,] #the type here is a list, bc it is a dropdown
br.form['ownerLastName'] = lastname
br.form['plateType'] = [plate,] #same as state
#br.form['verb'] = hiddenVal

#req = br.submit()

req = br.click(type="submit", nr=0)
res = br.open(req)


dom = lxml.html.fromstring(res.read())

getText = dom.cssselect('font')

answers = []

for x in getText:

    for z in x:
        answers.append(z.text)


answer = answers[0] #this is the result from the site.



if answer.startswith('No Search Results'):
    answer = 'No tickets today'
else:
    answer = 'Check the site, you got a ticket'

now = datetime.datetime.now(timezone('US/Central'))

today = now.strftime("%Y-%m-%d %H:%M:%S")

myData = []

myData.append({
            "date" : today,
            "answer" : answer
        
        })    
        


scraperwiki.sqlite.save(unique_keys=["date"], data=myData, table_name="ticketlog")
