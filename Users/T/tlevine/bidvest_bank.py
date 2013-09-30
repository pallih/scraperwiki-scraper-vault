from mechanize import Browser,make_response
from lxml.html import fromstring,tostring
from scraperwiki import swimport
from scraperwiki.sqlite import save,save_var,get_var,select,execute,show_tables
keyify=swimport('keyify').keyify
from time import time

DATE=time()
INPUT_IDS=('ob_iDdlddRegionTB','ctl00_cphLeftContent_ddRegion','ob_iDdlddBranchTB','ctl00_cphLeftContent_ddBranch')

def main():
  if get_var('step')==None:
    save_var('step',0)
  while get_var('step')!=None:
    if get_var('step')==0:
      download()
      save_var('step',1)
    elif get_var('step')==1:
      moreparsing_map()
      save_var('step',2)
    else:
      #Scraper is finished; reset
      save_var('step',None)

def moreparsing_map():
  "Map along the most recent results in the table (like a Couch map) and return a new one"
  d=select("* FROM `swdata` WHERE date_scraped=(SELECT max(date_scraped) from `swdata`);")
  for row in d:
    row['street-address'],row['postal-code']=splitAddress(row['Address_'])
    row['town']=extractTown(row['branchName'])
  if 'final' in show_tables():
    execute('DROP TABLE `final`;')

  d_final = []
  for row in d:
    if row['regionName'] not in ["Botswana", "Malawi", "Nambia"]:
      d_final.append(row)

  save([],d_final,'final')

def splitAddress(address):
  """Check whether the address contains a street address.
  If it does, split appropriately."""
  try:
    postcode=str(int(address.split(',')[-1]))
  except ValueError:
    #No postcode in address
    postcode=''
    streetAddress=address
  else:
    #Postcode in address
    streetAddress=','.join(address.split(',')[0:-1])

  return streetAddress,postcode

def extractTown(branchName):
  return branchName.split('-')[0].split('(')[0]

def download():
  b=BidvestBrowser()
  b.bvopen('http://www.bidvestbank.co.za/contact-us/Branch-Locator.aspx')
  b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] #This should go in __init__
  for regionName,regionId in b.getregions():
    b.selectregion(regionName,regionId)
    b.bvsubmit()
    for branchName,branchId in b.getbranches():
      b.selectregion(regionName,regionId)
      b.selectbranch(branchName,branchId)
      b.bvsubmit()
      branchinfo=b.getbranchinfo()

      #Save
      for row in branchinfo:
        row[0]=keyify(row[0])
      d=dict(branchinfo)
      d.update({
        'date_scraped':DATE
      , 'regionName':regionName
      , 'regionId':regionId
      , 'branchName':branchName
      , 'branchId':branchId
      })
      save([],d)

class BidvestBrowser(Browser):
  def bvopen(self,url):
    "Open the url and save the response text to self.r"
    r=self.open(url)
    self._process_response(r)

  def bvsubmit(self):
    r=self.submit()
    self._process_response(r)

  def _process_response(self,r):
    self.r=r.read()
    self.x=fromstring(self.r)
    self._writeable()

  def _writeable(self):
    "Make the form writeable"
    for id in INPUT_IDS:
      node=self.x.xpath('id("%s")' % id)[0]
      if node.attrib['type']=='hidden':
        node.attrib['type']='text'
      if 'readonly' in node.attrib:
        del(node.attrib['readonly'])

    #Save the changes
    response = make_response(
      tostring(self.x)
    , [("Content-Type", "text/html")]
    , self.geturl()
    , 200
    , "OK"
    )
    self.set_response(response)


  def getoptions(self,containerid):
    names=self.x.xpath('id("%s")/descendant::ul/li[position()>1]/b/text()' % containerid)
    ids=self.x.xpath('id("%s")/descendant::ul/li[position()>1]/i/text()' % containerid)
    return zip(names,ids)

  def getregions(self):
    return self.getoptions("ob_iDdlddRegionItemsContainer")

  def getbranches(self):
    return self.getoptions("ob_iDdlddBranchItemsContainer")

  def selectregion(self,name,id):
    self.select_form(nr=0)
    self['ob_iDdlddRegionTB']=name
    self['ctl00$cphLeftContent$ddRegion']=id

  def selectbranch(self,name,id):
    self.select_form(nr=0)
    self['ob_iDdlddBranchTB']=name
    self['ctl00$cphLeftContent$ddBranch']=id
    self.set_all_readonly(False)
    self["__EVENTTARGET"] = "ctl00$cphLeftContent$btnSend"
    self["__EVENTARGUMENT"] = ""

  def getbranchinfo(self):
    """Get branch info from the table; skip the first row (branch name) and map rows"""
    trs=self.x.xpath('//table/descendant::table/tr[position()>1][not(td/a/text()="View Map")]')
    tds_text=[]
    for tr in trs:
      tds=tr.xpath('td')
      td_text=['\n'.join(td.xpath('text()')) for td in tds]
      assert len(tds)==2
      tds_text.append(td_text)
    return tds_text

main()from mechanize import Browser,make_response
from lxml.html import fromstring,tostring
from scraperwiki import swimport
from scraperwiki.sqlite import save,save_var,get_var,select,execute,show_tables
keyify=swimport('keyify').keyify
from time import time

DATE=time()
INPUT_IDS=('ob_iDdlddRegionTB','ctl00_cphLeftContent_ddRegion','ob_iDdlddBranchTB','ctl00_cphLeftContent_ddBranch')

def main():
  if get_var('step')==None:
    save_var('step',0)
  while get_var('step')!=None:
    if get_var('step')==0:
      download()
      save_var('step',1)
    elif get_var('step')==1:
      moreparsing_map()
      save_var('step',2)
    else:
      #Scraper is finished; reset
      save_var('step',None)

def moreparsing_map():
  "Map along the most recent results in the table (like a Couch map) and return a new one"
  d=select("* FROM `swdata` WHERE date_scraped=(SELECT max(date_scraped) from `swdata`);")
  for row in d:
    row['street-address'],row['postal-code']=splitAddress(row['Address_'])
    row['town']=extractTown(row['branchName'])
  if 'final' in show_tables():
    execute('DROP TABLE `final`;')

  d_final = []
  for row in d:
    if row['regionName'] not in ["Botswana", "Malawi", "Nambia"]:
      d_final.append(row)

  save([],d_final,'final')

def splitAddress(address):
  """Check whether the address contains a street address.
  If it does, split appropriately."""
  try:
    postcode=str(int(address.split(',')[-1]))
  except ValueError:
    #No postcode in address
    postcode=''
    streetAddress=address
  else:
    #Postcode in address
    streetAddress=','.join(address.split(',')[0:-1])

  return streetAddress,postcode

def extractTown(branchName):
  return branchName.split('-')[0].split('(')[0]

def download():
  b=BidvestBrowser()
  b.bvopen('http://www.bidvestbank.co.za/contact-us/Branch-Locator.aspx')
  b.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] #This should go in __init__
  for regionName,regionId in b.getregions():
    b.selectregion(regionName,regionId)
    b.bvsubmit()
    for branchName,branchId in b.getbranches():
      b.selectregion(regionName,regionId)
      b.selectbranch(branchName,branchId)
      b.bvsubmit()
      branchinfo=b.getbranchinfo()

      #Save
      for row in branchinfo:
        row[0]=keyify(row[0])
      d=dict(branchinfo)
      d.update({
        'date_scraped':DATE
      , 'regionName':regionName
      , 'regionId':regionId
      , 'branchName':branchName
      , 'branchId':branchId
      })
      save([],d)

class BidvestBrowser(Browser):
  def bvopen(self,url):
    "Open the url and save the response text to self.r"
    r=self.open(url)
    self._process_response(r)

  def bvsubmit(self):
    r=self.submit()
    self._process_response(r)

  def _process_response(self,r):
    self.r=r.read()
    self.x=fromstring(self.r)
    self._writeable()

  def _writeable(self):
    "Make the form writeable"
    for id in INPUT_IDS:
      node=self.x.xpath('id("%s")' % id)[0]
      if node.attrib['type']=='hidden':
        node.attrib['type']='text'
      if 'readonly' in node.attrib:
        del(node.attrib['readonly'])

    #Save the changes
    response = make_response(
      tostring(self.x)
    , [("Content-Type", "text/html")]
    , self.geturl()
    , 200
    , "OK"
    )
    self.set_response(response)


  def getoptions(self,containerid):
    names=self.x.xpath('id("%s")/descendant::ul/li[position()>1]/b/text()' % containerid)
    ids=self.x.xpath('id("%s")/descendant::ul/li[position()>1]/i/text()' % containerid)
    return zip(names,ids)

  def getregions(self):
    return self.getoptions("ob_iDdlddRegionItemsContainer")

  def getbranches(self):
    return self.getoptions("ob_iDdlddBranchItemsContainer")

  def selectregion(self,name,id):
    self.select_form(nr=0)
    self['ob_iDdlddRegionTB']=name
    self['ctl00$cphLeftContent$ddRegion']=id

  def selectbranch(self,name,id):
    self.select_form(nr=0)
    self['ob_iDdlddBranchTB']=name
    self['ctl00$cphLeftContent$ddBranch']=id
    self.set_all_readonly(False)
    self["__EVENTTARGET"] = "ctl00$cphLeftContent$btnSend"
    self["__EVENTARGUMENT"] = ""

  def getbranchinfo(self):
    """Get branch info from the table; skip the first row (branch name) and map rows"""
    trs=self.x.xpath('//table/descendant::table/tr[position()>1][not(td/a/text()="View Map")]')
    tds_text=[]
    for tr in trs:
      tds=tr.xpath('td')
      td_text=['\n'.join(td.xpath('text()')) for td in tds]
      assert len(tds)==2
      tds_text.append(td_text)
    return tds_text

main()