import scraperwiki
import time
import random
import mechanize
from datetime import datetime

from BeautifulSoup import BeautifulSoup
import os

data = [
          {'start_url':'http://apps.countycarlow.ie/ePlan41/SearchListing.aspx', 'search_url':'http://apps.countycarlow.ie/ePlan41/SearchResults.aspx', 'county':'Carlow', 'base_url':'http://apps.countycarlow.ie/ePlan41/'}
          ,{'start_url':'http://www.cavancoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.cavancoco.ie/eplan41/SearchResults.aspx', 'county':'Cavan', 'base_url':'http://www.cavancoco.ie/eplan41/'}
          ,{'start_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/SearchListing.aspx', 'search_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/SearchResults.aspx', 'county':'Clare', 'base_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/'}
          ,{'start_url':'http://www.laois.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.laois.ie/eplan41/SearchResults.aspx', 'county':'Laois', 'base_url':'http://www.laois.ie/eplan41/'}
          #,{'start_url':'http://193.178.1.87/ePlan41/SearchListing.aspx', 'search_url':'http://193.178.1.87/ePlan41/SearchResults.aspx', 'county':'Leitrim', 'base_url':'http://193.178.1.87/ePlan41/'}
          ,{'start_url':'http://www.longfordcoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.longfordcoco.ie/eplan41/SearchResults.aspx', 'county':'Longford', 'base_url':'http://www.longfordcoco.ie/eplan41/'}
        ,{'start_url':'http://www.louthcoco.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.louthcoco.ie/ePlan41/SearchResults.aspx', 'county':'Louth', 'base_url':'http://www.louthcoco.ie/ePlan41/'}
        ,{'start_url':'http://www.meath.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.meath.ie/ePlan41/SearchResults.aspx', 'county':'Meath', 'base_url':'http://www.meath.ie/ePlan41/'}
         ,{'start_url':'http://www.monaghan.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.monaghan.ie/ePlan41/SearchResults.aspx', 'county':'Monaghan', 'base_url':'http://www.monaghan.ie/ePlan41/'}
         ,{'start_url':'http://www.offaly.ie/eplan/SearchListing.aspx', 'search_url':'http://www.offaly.ie/eplan/SearchResults.aspx', 'county':'Offaly', 'base_url':'http://www.offaly.ie/eplan/'}
         ,{'start_url':'http://www.roscommoncoco.ie/eplan/SearchListing.aspx', 'search_url':'http://www.roscommoncoco.ie/eplan/SearchResults.aspx', 'county':'Roscommon', 'base_url':'http://www.roscommoncoco.ie/eplan/'}
        ,{'start_url':'http://www.tipperarynorth.ie/ePlan40/SearchListing.aspx', 'search_url':'http://www.tipperarynorth.ie/ePlan40/SearchResults.aspx', 'county':'NTipperary', 'base_url':'http://www.tipperarynorth.ie/ePlan40/'}
        ,{'start_url':'http://www.westmeathcoco.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.westmeathcoco.ie/ePlan41/SearchResults.aspx', 'county':'Westmeath', 'base_url':'http://www.westmeathcoco.ie/ePlan41/'}
        ,{'start_url':'http://www.southtippcoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.southtippcoco.ie/eplan41/SearchResults.aspx', 'county':'STipperary','base_url':'http://www.southtippcoco.ie/eplan41/'}
        ,{'start_url':'http://www.sligococo.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.sligococo.ie/eplan41/SearchResults.aspx', 'county':'Sligo','base_url':'http://www.sligococo.ie/ePlan41/'}
        ,{'start_url':'http://www.limerickcity.ie/ePlan/SearchListing.aspx', 'search_url':'http://www.limerickcity.ie/ePlan/SearchResults.aspx', 'county':'LimerickCity','base_url':'http://www.limerickcity.ie/ePlan/'}
        ,{'start_url':'http://www.wicklow.ie/eplan41/SearchListing.aspx',  'search_url':'http://www.wicklow.ie/eplan41/SearchResults.aspx', 'county':'Wicklow', 'base_url':'http://www.wicklow.ie/eplan41/'}
       ]

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.17) Gecko/20110420 Firefox/3.6.17 (.NET CLR 3.5.30729)'
br = mechanize.Browser()
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def get_first_page(start_url,search_url,county,base_url):
  response = br.open(start_url)
  response.read()
  try:
    br.select_form("aspnetForm")
  except :
    #some of the websites don't provide the form name. if form name is not there, use the first form
    br.form = list(br.forms())[0]
  #set the form action correctly. in eplan41 this is et through Javascript
  br.form.action = search_url
  #get only the last 7 days (it is 21 by default)
  for c in br.form.controls:
    if c.name=='ctl00$MainContentPlaceHolder$rdoList_ReportInterval':
      c.readonly = False
      c.value = ['7']
  response = br.submit()
  html = response.read()
  #save apps
  num_of_pages = get_number_of_pages(html)
  handle_page(html,county,base_url,num_of_pages>1)
  return num_of_pages
  

def get_page(page_number,county,base_url):
  try:
    br.select_form("aspnetForm")
  except :
    #some of the websites don't provide the form name. if form name is not there, use the first form
    br.form = list(br.forms())[0]
  print(page_number)
  for c in br.form.controls:
    if c.name == '__EVENTARGUMENT':
      c.readonly = False
      c.value = 'Page$' + str(page_number)
    if c.name == '__EVENTTARGET':
      c.readonly = False
      c.value = 'ctl00$MainContentPlaceHolder$gvResults'
  res = br.submit()
  html = res.read()
  handle_page(html,county,base_url)

def get_number_of_pages(html):
  soup = BeautifulSoup(html)
  try:
    last_td = soup.find('tr',{'class':'PagerTableSettings'}).find('td').findAll('td')[-1]
    return last_td.find('a').text
  except:
    #error means only one page... (hopefully)
    return 1

def handle_page(html,county,base,multiple_pages=True):
  soup = BeautifulSoup(html)
  try:
    trs = soup.find('table',{'id':'ctl00_MainContentPlaceHolder_gvResults'}).findAll('tr',{},False)
    if multiple_pages:
      #the first and last rows are the page numbers... drop them out
      trs = trs[2:-1]
    else:
      trs = trs[1:]
    for tr in trs:
      app_info = tr.find('td').find('a')
      app_id = app_info.text
      app_url = base + app_info['href']
      #scraperwiki.sqlite.save(['APP_ID','County'],{'APP_ID':app_id,'APP_URL':app_url,'County':county})
      handle_app(app_url,app_id,county)
  except:
    #no applications can be found
    None

def handle_app(url,id,county):
  print('handling ' + url)
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  description = get_td_content(soup, 'Development Description:')
  address = get_td_content(soup, 'Development Address:')
  northing = get_td_content(soup, 'Grid Northings:','0')
  easting = get_td_content(soup, 'Grid Eastings:','0')
  app_date = parse_date(get_td_content(soup, 'Received Date:'))
  applicant_name = get_td_content(soup, 'Applicant Name:')
  pos_lat = ''
  pos_long = ''
  try:
    lat_long = get_lat_long(float(easting), float(northing))
    pos_lat =lat_long[0]
    pos_long = lat_long[1]
  except:
    pos_lat = None
    pos_long = None
  scraperwiki.sqlite.save(['appref','county'],{'appref':id, 'url':url, 'county':county, 'details':description, 'address':address, 'date':app_date, 'applicant':applicant_name, 'lat':pos_lat, 'lng':pos_long})
  time.sleep(random.uniform(0.5,1.5))

def get_td_content(soup,th_content,default_val=''):
  try:
    th = soup.find('th',text=th_content).parent
    tds = th.findNextSiblings('td')
    return tds[0].text
  except:
    #allow silent failure
    return default_val
def get_lat_long(easting,northing):
  if easting == 0 or northing == 0:
    return [None, None]
  oscoord = scraperwiki.geo.turn_eastingnorthing_into_osie36(easting, northing)
  lat_long = scraperwiki.geo.turn_osie36_into_wgs84(oscoord[0], oscoord[1], 200)
  print lat_long
  return lat_long[0:2]

def parse_date(date_str):
  return datetime.strptime(date_str,'%d/%m/%Y').date()
#start
for d in data:
  num_of_pages = int(get_first_page(d['start_url'], d['search_url'],d['county'],d['base_url']))
  print ('working on ' + d['county'])
  for i in range(2,num_of_pages+1):
    get_page(i,d['county'],d['base_url'])

import scraperwiki
import time
import random
import mechanize
from datetime import datetime

from BeautifulSoup import BeautifulSoup
import os

data = [
          {'start_url':'http://apps.countycarlow.ie/ePlan41/SearchListing.aspx', 'search_url':'http://apps.countycarlow.ie/ePlan41/SearchResults.aspx', 'county':'Carlow', 'base_url':'http://apps.countycarlow.ie/ePlan41/'}
          ,{'start_url':'http://www.cavancoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.cavancoco.ie/eplan41/SearchResults.aspx', 'county':'Cavan', 'base_url':'http://www.cavancoco.ie/eplan41/'}
          ,{'start_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/SearchListing.aspx', 'search_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/SearchResults.aspx', 'county':'Clare', 'base_url':'http://www.clarecoco.ie/planning/planning-applications/search-planning-applications/'}
          ,{'start_url':'http://www.laois.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.laois.ie/eplan41/SearchResults.aspx', 'county':'Laois', 'base_url':'http://www.laois.ie/eplan41/'}
          #,{'start_url':'http://193.178.1.87/ePlan41/SearchListing.aspx', 'search_url':'http://193.178.1.87/ePlan41/SearchResults.aspx', 'county':'Leitrim', 'base_url':'http://193.178.1.87/ePlan41/'}
          ,{'start_url':'http://www.longfordcoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.longfordcoco.ie/eplan41/SearchResults.aspx', 'county':'Longford', 'base_url':'http://www.longfordcoco.ie/eplan41/'}
        ,{'start_url':'http://www.louthcoco.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.louthcoco.ie/ePlan41/SearchResults.aspx', 'county':'Louth', 'base_url':'http://www.louthcoco.ie/ePlan41/'}
        ,{'start_url':'http://www.meath.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.meath.ie/ePlan41/SearchResults.aspx', 'county':'Meath', 'base_url':'http://www.meath.ie/ePlan41/'}
         ,{'start_url':'http://www.monaghan.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.monaghan.ie/ePlan41/SearchResults.aspx', 'county':'Monaghan', 'base_url':'http://www.monaghan.ie/ePlan41/'}
         ,{'start_url':'http://www.offaly.ie/eplan/SearchListing.aspx', 'search_url':'http://www.offaly.ie/eplan/SearchResults.aspx', 'county':'Offaly', 'base_url':'http://www.offaly.ie/eplan/'}
         ,{'start_url':'http://www.roscommoncoco.ie/eplan/SearchListing.aspx', 'search_url':'http://www.roscommoncoco.ie/eplan/SearchResults.aspx', 'county':'Roscommon', 'base_url':'http://www.roscommoncoco.ie/eplan/'}
        ,{'start_url':'http://www.tipperarynorth.ie/ePlan40/SearchListing.aspx', 'search_url':'http://www.tipperarynorth.ie/ePlan40/SearchResults.aspx', 'county':'NTipperary', 'base_url':'http://www.tipperarynorth.ie/ePlan40/'}
        ,{'start_url':'http://www.westmeathcoco.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.westmeathcoco.ie/ePlan41/SearchResults.aspx', 'county':'Westmeath', 'base_url':'http://www.westmeathcoco.ie/ePlan41/'}
        ,{'start_url':'http://www.southtippcoco.ie/eplan41/SearchListing.aspx', 'search_url':'http://www.southtippcoco.ie/eplan41/SearchResults.aspx', 'county':'STipperary','base_url':'http://www.southtippcoco.ie/eplan41/'}
        ,{'start_url':'http://www.sligococo.ie/ePlan41/SearchListing.aspx', 'search_url':'http://www.sligococo.ie/eplan41/SearchResults.aspx', 'county':'Sligo','base_url':'http://www.sligococo.ie/ePlan41/'}
        ,{'start_url':'http://www.limerickcity.ie/ePlan/SearchListing.aspx', 'search_url':'http://www.limerickcity.ie/ePlan/SearchResults.aspx', 'county':'LimerickCity','base_url':'http://www.limerickcity.ie/ePlan/'}
        ,{'start_url':'http://www.wicklow.ie/eplan41/SearchListing.aspx',  'search_url':'http://www.wicklow.ie/eplan41/SearchResults.aspx', 'county':'Wicklow', 'base_url':'http://www.wicklow.ie/eplan41/'}
       ]

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.17) Gecko/20110420 Firefox/3.6.17 (.NET CLR 3.5.30729)'
br = mechanize.Browser()
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def get_first_page(start_url,search_url,county,base_url):
  response = br.open(start_url)
  response.read()
  try:
    br.select_form("aspnetForm")
  except :
    #some of the websites don't provide the form name. if form name is not there, use the first form
    br.form = list(br.forms())[0]
  #set the form action correctly. in eplan41 this is et through Javascript
  br.form.action = search_url
  #get only the last 7 days (it is 21 by default)
  for c in br.form.controls:
    if c.name=='ctl00$MainContentPlaceHolder$rdoList_ReportInterval':
      c.readonly = False
      c.value = ['7']
  response = br.submit()
  html = response.read()
  #save apps
  num_of_pages = get_number_of_pages(html)
  handle_page(html,county,base_url,num_of_pages>1)
  return num_of_pages
  

def get_page(page_number,county,base_url):
  try:
    br.select_form("aspnetForm")
  except :
    #some of the websites don't provide the form name. if form name is not there, use the first form
    br.form = list(br.forms())[0]
  print(page_number)
  for c in br.form.controls:
    if c.name == '__EVENTARGUMENT':
      c.readonly = False
      c.value = 'Page$' + str(page_number)
    if c.name == '__EVENTTARGET':
      c.readonly = False
      c.value = 'ctl00$MainContentPlaceHolder$gvResults'
  res = br.submit()
  html = res.read()
  handle_page(html,county,base_url)

def get_number_of_pages(html):
  soup = BeautifulSoup(html)
  try:
    last_td = soup.find('tr',{'class':'PagerTableSettings'}).find('td').findAll('td')[-1]
    return last_td.find('a').text
  except:
    #error means only one page... (hopefully)
    return 1

def handle_page(html,county,base,multiple_pages=True):
  soup = BeautifulSoup(html)
  try:
    trs = soup.find('table',{'id':'ctl00_MainContentPlaceHolder_gvResults'}).findAll('tr',{},False)
    if multiple_pages:
      #the first and last rows are the page numbers... drop them out
      trs = trs[2:-1]
    else:
      trs = trs[1:]
    for tr in trs:
      app_info = tr.find('td').find('a')
      app_id = app_info.text
      app_url = base + app_info['href']
      #scraperwiki.sqlite.save(['APP_ID','County'],{'APP_ID':app_id,'APP_URL':app_url,'County':county})
      handle_app(app_url,app_id,county)
  except:
    #no applications can be found
    None

def handle_app(url,id,county):
  print('handling ' + url)
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  description = get_td_content(soup, 'Development Description:')
  address = get_td_content(soup, 'Development Address:')
  northing = get_td_content(soup, 'Grid Northings:','0')
  easting = get_td_content(soup, 'Grid Eastings:','0')
  app_date = parse_date(get_td_content(soup, 'Received Date:'))
  applicant_name = get_td_content(soup, 'Applicant Name:')
  pos_lat = ''
  pos_long = ''
  try:
    lat_long = get_lat_long(float(easting), float(northing))
    pos_lat =lat_long[0]
    pos_long = lat_long[1]
  except:
    pos_lat = None
    pos_long = None
  scraperwiki.sqlite.save(['appref','county'],{'appref':id, 'url':url, 'county':county, 'details':description, 'address':address, 'date':app_date, 'applicant':applicant_name, 'lat':pos_lat, 'lng':pos_long})
  time.sleep(random.uniform(0.5,1.5))

def get_td_content(soup,th_content,default_val=''):
  try:
    th = soup.find('th',text=th_content).parent
    tds = th.findNextSiblings('td')
    return tds[0].text
  except:
    #allow silent failure
    return default_val
def get_lat_long(easting,northing):
  if easting == 0 or northing == 0:
    return [None, None]
  oscoord = scraperwiki.geo.turn_eastingnorthing_into_osie36(easting, northing)
  lat_long = scraperwiki.geo.turn_osie36_into_wgs84(oscoord[0], oscoord[1], 200)
  print lat_long
  return lat_long[0:2]

def parse_date(date_str):
  return datetime.strptime(date_str,'%d/%m/%Y').date()
#start
for d in data:
  num_of_pages = int(get_first_page(d['start_url'], d['search_url'],d['county'],d['base_url']))
  print ('working on ' + d['county'])
  for i in range(2,num_of_pages+1):
    get_page(i,d['county'],d['base_url'])

