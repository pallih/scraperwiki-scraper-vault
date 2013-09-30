from requests import get
from string import ascii_lowercase
from lxml.html import fromstring
from scraperwiki import swimport
from scraperwiki.sqlite import save,select,get_var,save_var,execute
keyify=swimport('keyify').keyify
from time import time
import re

DATE=time()

def main():
  if None==get_var('downloaded'):
    download()
    save_var('downloaded',1)
  execute('DROP TABLE IF EXISTS `final`')
  clean()
  save_var('downloaded',None)

def clean():
  d=select('* FROM `swdata` WHERE `date_scraped`=(SELECT max(`date_scraped`) FROM `swdata`);')
  POSTCODE=re.compile(r'[0-9]*$')
  for row in d:
    row['postcode']=re.findall(POSTCODE,row['Postal_Address'])[0]
  save([],d,'final')

def download():
  d=[]
  for letter in ascii_lowercase:
    x=search_letter(letter)
    branch_tables=x.cssselect('table.locatorTable table')
    d_letter=[extract_branch_info(branch_table) for branch_table in branch_tables]

    for record in d_letter:
      record['url']=searchurl(letter)
      record['date_scraped']=DATE

    d.extend(d_letter)
  save([],d)

def searchurl(letter):
  return "https://www.fnb.co.za/phcontrollers/BranchSearch?searchString=%s*&filterPremier=false&filterEasyPlan=false&filterBranch=false&filterPrivate=false" % letter

def search_letter(letter,verbose=False):
  r=get(searchurl(letter),headers={"Referer":"https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"})
  if verbose:
    print(r.content)
  return fromstring(r.content)

def extract_branch_info(branch_table):
  record={}

  #Name
  record['name']=extract_branch_name(branch_table)

  #Table
  trs=branch_table.xpath('tr[count(td)=2]')
  for tr in trs:
    tds=tr.xpath('td')
    key=keyify(tds[0].text)
    value=tds[1].text
    record[key]=value
  return record

def extract_branch_name(branch_table):
  "Not actually in the table"
  namedisplay=branch_table.xpath('../../preceding-sibling::tr[position()=1]/td[@class="namedisplay"]')
  assert len(namedisplay)==1
  return namedisplay[0].text_content()

#def start_session():
#  s=session()
#  s.headers={
#    "Accept":"*/*"
#  , "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
#  , "Accept-Encoding":"gzip,deflate,sdch"
#  , "Accept-Language":"en-US,en;q=0.8"
#  , "Connection":"keep-alive"
#Cookie:X-Mapping-fpbmgbaj=71D2C7C829467C10B6AFE31C713DEBC8; __utmz=169205494.1327782123.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html; menuHist=%0A/02navigation/global/ajaxGlobal/MENU-useful-stuff.html*undefined%0A/02navigation/global/ajaxGlobal/MENU-personal.html*undefined; JSESSIONID=6A99978EED894FAA3D62C8D3D87B4DA3; mycookietrail=Branch%20Locator*https%3A//www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html%0AWe%20have%20encountered%20an%20error*https%3A//www.fnb.co.za/contact-us/locators/branchLocator/%0A; __utma=169205494.351131272.1327782123.1327782123.1327810497.2; __utmc=169205494; __utmb=169205494.2.10.1327810497
#  , "Host":"www.fnb.co.za"
#  , "Referer":"https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"
#  , "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7"
#  }
#  s.headers["Referer"]="https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"
#  return s

main()from requests import get
from string import ascii_lowercase
from lxml.html import fromstring
from scraperwiki import swimport
from scraperwiki.sqlite import save,select,get_var,save_var,execute
keyify=swimport('keyify').keyify
from time import time
import re

DATE=time()

def main():
  if None==get_var('downloaded'):
    download()
    save_var('downloaded',1)
  execute('DROP TABLE IF EXISTS `final`')
  clean()
  save_var('downloaded',None)

def clean():
  d=select('* FROM `swdata` WHERE `date_scraped`=(SELECT max(`date_scraped`) FROM `swdata`);')
  POSTCODE=re.compile(r'[0-9]*$')
  for row in d:
    row['postcode']=re.findall(POSTCODE,row['Postal_Address'])[0]
  save([],d,'final')

def download():
  d=[]
  for letter in ascii_lowercase:
    x=search_letter(letter)
    branch_tables=x.cssselect('table.locatorTable table')
    d_letter=[extract_branch_info(branch_table) for branch_table in branch_tables]

    for record in d_letter:
      record['url']=searchurl(letter)
      record['date_scraped']=DATE

    d.extend(d_letter)
  save([],d)

def searchurl(letter):
  return "https://www.fnb.co.za/phcontrollers/BranchSearch?searchString=%s*&filterPremier=false&filterEasyPlan=false&filterBranch=false&filterPrivate=false" % letter

def search_letter(letter,verbose=False):
  r=get(searchurl(letter),headers={"Referer":"https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"})
  if verbose:
    print(r.content)
  return fromstring(r.content)

def extract_branch_info(branch_table):
  record={}

  #Name
  record['name']=extract_branch_name(branch_table)

  #Table
  trs=branch_table.xpath('tr[count(td)=2]')
  for tr in trs:
    tds=tr.xpath('td')
    key=keyify(tds[0].text)
    value=tds[1].text
    record[key]=value
  return record

def extract_branch_name(branch_table):
  "Not actually in the table"
  namedisplay=branch_table.xpath('../../preceding-sibling::tr[position()=1]/td[@class="namedisplay"]')
  assert len(namedisplay)==1
  return namedisplay[0].text_content()

#def start_session():
#  s=session()
#  s.headers={
#    "Accept":"*/*"
#  , "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
#  , "Accept-Encoding":"gzip,deflate,sdch"
#  , "Accept-Language":"en-US,en;q=0.8"
#  , "Connection":"keep-alive"
#Cookie:X-Mapping-fpbmgbaj=71D2C7C829467C10B6AFE31C713DEBC8; __utmz=169205494.1327782123.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html; menuHist=%0A/02navigation/global/ajaxGlobal/MENU-useful-stuff.html*undefined%0A/02navigation/global/ajaxGlobal/MENU-personal.html*undefined; JSESSIONID=6A99978EED894FAA3D62C8D3D87B4DA3; mycookietrail=Branch%20Locator*https%3A//www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html%0AWe%20have%20encountered%20an%20error*https%3A//www.fnb.co.za/contact-us/locators/branchLocator/%0A; __utma=169205494.351131272.1327782123.1327782123.1327810497.2; __utmc=169205494; __utmb=169205494.2.10.1327810497
#  , "Host":"www.fnb.co.za"
#  , "Referer":"https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"
#  , "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7"
#  }
#  s.headers["Referer"]="https://www.fnb.co.za/contact-us/locators/branchLocator/frontEndEnh.html"
#  return s

main()