#!/usr/bin/env python2
"""

## Notes

### Website technical overview
First, you make a GET request to load the menu.

Thereafter, you make AJAX POST requests to load a box containing both
* The "Select a City" drop-down
* The branch results

### This stuff never changes

    Business hours:  Mondays to Fridays from 8:30am to 5:00pm 
    Saturdays from 8:00am - 12:00pm
    Central enquiries:  086 00 22 932 from 8:00am to 5:00pm

## Stuff that might be useful
re.findall(r'j_id_jsp_[0-9]*_[^,\']*',b.r.content)

"""

from lxml.html import fromstring
from requests import Session
from json import dumps
import warnings
import re
from time import time
DATE=time()

#from scraperwiki import swimport
#swimport('keyify').keyify
def keyify(raw):
  return raw.replace(' ','_')

try:
  from scraperwiki.sqlite import save
except ImportError:
  def save(a,b,c):
    print b
  is_scraperwiki=False
else:
  is_scraperwiki=True

URLS={
  "start":"https://www.africanbank.co.za/default.jsf?page_id=170"
, "continue":"https://www.africanbank.co.za/default9.jsf"
}

def main():
  b=B()
  b.menu()
  provinces=b.getprovinces()
  for province in provinces:
    b.province(province)
    cities=b.getcities()
    for city in cities:
      b.city(city)
      branches=b.getbranches()
      savebranches(branches,city,province)

def test_form_elements(b,step,check="cities"):
  if check=="provinces":
    assert b.x.xpath('count(id("branchLocator:branchLocatorForm:provinceList"))')==1, "Province list didn't load at %s step." %step
  elif check=="cities":
    assert b.x.xpath('count(id("branchLocator:branchLocatorForm:citiesList"))')==1, "Cities list didn't load at %s step." % step

def test():
  b=B()
  b.menu()
  test_form_elements(b,"menu",check="provinces")

  provinces=b.getprovinces()
  assert len(provinces)>0, "No provinces detected"
  print("Detected these provinces:")
  print provinces

  b.province(provinces[0])
  #test_form_elements(b,"province")

  cities=b.getcities()
  assert len(cities)>0, "No cities detected"
  print("Detected these cities:")
  print(cities)

  b.city(cities[0])
  #test_form_elements(b,"branch")

  branches=b.getbranches()
  assert len(branches)>0, "No branches detected"
  print("Detected these branches:")
  print(branches)

  #If there hasn't been an error yet
  print("The full directory has been descended without apparent error; the scraper seems to work.")

def savebranches(branches,city,province):
  if len(branches)==0:
    warnings.warn("No branches detected for %s, %s" %(city['cityName'],province['provinceName']) ) 
  else:
    for branch in branches:
      branch.update(city)
      branch.update(province)
      branch['date_scraped']=DATE
    save([],branches,'branches')

class B(Session):
  #"Browse the African Bank branches menu"
  def menu(self):
    "Open the menu"
    self.r=self.get(URLS['start'],verify=False)
    self.loadxml()

  def submit(self):
    self.r=self.post(URLS['continue'],self.p,verify=False)
    self.loadxml()

  def loadxml(self):
    try:
      self.x=fromstring(self.r.content)
    except Exception,e:
      self.record_error(e,"request content decoding")
      raise

  def record_error(self,error_detail,error_at):
    save([],{
      "request":dumps(self.r.request.data)
    , "request_content":self.r.content
    , "error_detail":error_detail
    , "error_at":error_at
    },'errors')

  def province(self,province):
    "Takes a dict with provinceName and provinceId"
    self.p={
      "AJAXREQUEST":"j_id_jsp_1880908480_0"
    , "branchLocator:branchLocatorForm":"branchLocator:branchLocatorForm"
    , "branchLocator:branchLocatorForm:provinceList":province["provinceId"]
    , "branchLocator:branchLocatorForm:branchSelected":""
    , "branchLocator:branchLocatorForm:contactMethod":"sms"
    , "branchLocator:branchLocatorForm:mobilePhoneNoCode":""
    , "branchLocator:branchLocatorForm:mobilePhoneNo":""
    , "branchLocator:branchLocatorForm:emailAddress":""
    , "javax.faces.ViewState":"j_id1"
    , "branchLocator:branchLocatorForm:j_id_jsp_883344110_5pc2":"branchLocator:branchLocatorForm:j_id_jsp_883344110_5pc2"
    , "":""
    }
    self.submit()

  def city(self,city):
    "Takes a dict with cityName and cityId"
    self.p.update({
      "branchLocator:branchLocatorForm:citiesList":city['cityName']
    , "branchLocator:branchLocatorForm:j_id_jsp_883344110_10pc2":"branchLocator:branchLocatorForm:j_id_jsp_883344110_10pc2"
    })
    self.submit()

  def getprovinces(self):
    options=self.x.xpath('id("branchLocator:branchLocatorForm:provinceList")/option[@value!="0"]')
    return [dict(zip(["provinceId","provinceName"],option.xpath('attribute::value')+option.xpath('text()'))) for option in options]

  def getcities(self):
    options=self.x.xpath('id("branchLocator:branchLocatorForm:citiesList")/option[@value!="0"]')
    cities=[]
    for option in options:
      city=dict(zip(["cityId","cityName"],option.xpath('attribute::value')+option.xpath('text()')))
      cities.append(city)
    return cities
    
  def getbranches(self):
    header_xpath='id("branchLocator:branchLocatorForm:branchesTableRich")/thead/tr/th[position()>1]'
    header=map(keyify,[th.text_content() for th in self.x.xpath(header_xpath)])

    rows_xpath='id("branchLocator:branchLocatorForm:branchesTableRich")/tbody/tr'
    rows=[tr.xpath('td[position()>1]/text()') for tr in self.x.xpath(rows_xpath)]

    return [dict(zip(header,row)) for row in rows]

if __name__=="__main__" or is_scraperwiki:
  main()
  #test()
