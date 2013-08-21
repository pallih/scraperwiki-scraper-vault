from requests import get,post
from lxml.html import fromstring,tostring
from re import sub
from time import time
try:
  from scraperwiki import swimport
  from scraperwiki.sqlite import save,get_var,save_var
except ImportError:
  def save(a,b,c):
    print(b)

  __VARS={}
  def get_var(a):
    if __VARS.has_key(a):
      return __VARS[a]
  def save_var(a,b):
    __VARS[a]=b

  def options(*args,**kwargs):
    return [{"branchId":"174","branchName":"DUNNO"}]
else:
  options=swimport('options').options

URL="http://www.postbank.co.za/contact.aspx?ID=3"

def log(foo):
  print(foo)

if get_var('previous_branchId')==None:
  save_var('DATE',time())
  FIRST_RUN=True
else:
  FIRST_RUN=False

DATE=get_var('DATE')

def main():
  b=PostbankBrowser()
  branches=b.get_branch_list()
  if FIRST_RUN:
    save_branches(branches)

  for branchId in select_branchIds(branches):
    b.load_branch(branchId)
    d=b.get_branch_info()
    d['branchId']=branchId
    save([],d,'branch_info')
    save_var('previous_branchId',branchId)

  save_var('previous_branchId',None)

def select_branchIds(branches):
  branchIds=[unicode(branch['branchId']) for branch in branches]
  previous_branchId=get_var('previous_branchId')
  branchIds.sort()
  i=branchIds.index(previous_branchId)
  return branchIds[i:]

def save_branches(branches):
  for branch in branches:
    branch['date_scraped']=DATE
  save([],branches,'branch_names')

class PostbankBrowser():
  def __init__(self):
    self.x=fromstring(get(URL).content)

  def get_branch_list(self):
    select=self.x.get_element_by_id("Centralcolum3_drpFAQ")
    o=options(select,valuename="branchId",textname="branchName",ignore_value="Please select...")
    for option in o:
      option['branchName']=PostbankBrowser.compact(option['branchName'])
    return o

  def get_branch_info(self):
    row={}
    row['date_scraped']=DATE
    trs=self.x.xpath('id("Centralcolum3_dtgGroup")/descendant::tr[td/*[self::span or self::strong]]')[:-1] #Skip the junk last row
    for tr in trs:
      tds=tr.xpath('td')
      if len(tds)==1:
        td=tds[0]
        if 2==td.xpath('count(span/b/text())'):
          row['loc1'],row['loc2']=[PostbankBrowser.compact(text) for text in td.xpath('span/b/text()')]
        else:
          log(tostring(td))

      elif len(tds)==2:
        cells=tr.xpath('td/*[self::span or self::strong]')
        key=cells[0].text
        value=cells[1].text

        for thing in [key,value]:
          if thing==None:
            thing=""
          else:
            thing=PostbankBrowser.compact(thing)

        row[key]=value
      else:
        raise self.TableRowError(tostring(tr))
    return row


  def viewstate(self):
    return self.x.xpath('id("__VIEWSTATE")/@value')[0]

  def eventvalidation(self):
    return self.x.xpath('id("__EVENTVALIDATION")/@value')[0]

  def load_branch(self,branchId):
    self.x=fromstring(post(URL,{
      "__EVENTTARGET":""
    , "__EVENTARGUMENT":""
    , "__LASTFOCUS":""
    , "__VIEWSTATE":self.viewstate()
    , "Iwantto":"-------Please select--------"
    , "menu$txtSearch":""
    , "Centralcolum3$drpFAQ":branchId
    , "Centralcolum3$btnSubmit.x":29
    , "Centralcolum3$btnSubmit.y":11
    , "Centralcolum3$txtown":""
    , "__EVENTVALIDATION":self.eventvalidation()
    }).content)

  class TableRowError(Exception):
    pass

  @staticmethod
  def compact(string):
    for char in ('\n','\t','\r'):
      string=string.replace(char,' ')
    for regex in (r'  +',r'^ *',r' *$'):
      string=sub(regex,'',string)
    return string

def _test_compact():
  assert 1==len(PostbankBrowser.compact(' oaeuo     aoeui ').split(' '))

main()