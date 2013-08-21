from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime
from geopy import geocoders

def ScrapeIncident(site, link):
    page = urlopen(link)
    rawtext = page.read()
    html = fromstring(rawtext)
    #print tostring(html)
    table = html.cssselect('table')[0]

    ROW_NAMES = [th.text_content().strip() for th in table.cssselect('th')]
    for i in range(len(ROW_NAMES)):
        ROW_NAMES[i]= ROW_NAMES[i].replace('#','num')
        ROW_NAMES[i]= ROW_NAMES[i].replace(' ','_')
        ROW_NAMES[i]= ROW_NAMES[i].replace('.','')

    cellvalues = []
    for tr in table.cssselect('tr'):
        cellvalues.extend([td.text_content().strip() for td in tr.cssselect('td')])
    data= dict(zip(ROW_NAMES,cellvalues))

   
    data['Dispatch_num'] = int(data['Dispatch_num'])

    try:
        data['Incident_num'] = int(data['Incident_num'])
    except:
        print 'Incident_num is not entered, will replace with 0'
        data['Incident_num'] = 0
    try:
        data['Location_Apt_num'] = int(data['Location_Apt_num'])
    except:
        print 'Location_Apt_num is not entered, will replace with 0'
        data['Location_Apt_num'] = 0

    data['Dispatch_day'] = datetime.datetime.strptime(data['Dispatch_Time'], '%m/%d/%Y %I:%M:%S %p').date()
    data['Dispatch_Time'] = datetime.datetime.strptime(data['Dispatch_Time'], '%m/%d/%Y %I:%M:%S %p').time()
   

    save(['Dispatch_num'],data)
    
def main():
    site ='http://www.iowa-city.org/icgov/apps/police/neighborhood.asp'
    mainpage = urlopen(site)
    rawtext = mainpage.read()
    html = fromstring(rawtext)
    
    table = html.cssselect('table')[0]

    for tr in table.cssselect('tr')[1:5]:
        link = tr.cssselect('a')[0]
        link = site + link.attrib['href']
        print link
        ScrapeIncident(site, link)
main()