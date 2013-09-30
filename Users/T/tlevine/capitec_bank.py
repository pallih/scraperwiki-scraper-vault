from requests import post,get
from lxml.html import fromstring,tostring
from scraperwiki.sqlite import save, select, execute, commit
from scraperwiki import swimport
options=swimport('options').options
from re import findall,sub
from demjson import decode as loads
from time import time

DATE=time()

def download(verbose=True):
  provinces=get_province_list()
  if verbose:
    print("Found these provinces:")
    print(provinces)
  for province in provinces:
    if verbose:
      print("Entering this province:")
      print(province)
    branches=get_branch_list(province['provinceId'])
    if verbose:
      print("Found these branches:")
      print(branches)
    for branch in branches:
      if verbose:
        print("Entering this branch:")
        print(branch)
      branch.update(province)
    for branch in branches:
      branch['date-scraped']=DATE
    save([],branches,'branches')

def get_province_list():
  x=load_request(request_province_list())
  o=options(x.get_element_by_id("searchProvince"),ignore_text="Province",textname="provinceName",valuename="provinceId")
  return o

def get_branch_list(provinceId):
  x=load_request(request_province_branches(provinceId))
  branches=[]
  for branchBlock in x.cssselect('.branchBlock'):
    d=branchBlock_info(branchBlock)
    branches.append(d)
  return branches


def branchBlock_info(branchBlock):
  """It's one of these

      <div class="branchBlock">
        <h3>Bushbuckridge</h3>
        <p><span class="infoAddr">Shop 4<br />Bushbuckridge Shopping Centre, Bushbuckridge, 1280</span></p>
        <p><span class="infoTel">0860 10 20 43</span> <span class="infoEmail"><a href="mailto:clientcare@capitecbank.co.za" class="trackView" >clientcare@capitecbank.co.za</a></span> <span class="infoViewMap"><a href="#gmap" class="viewOnMap" onclick="javascript:showInfoWindow({ 'branchId': 74 },-24.834183,31.069195);" >View on Map</a></span></p>
      </div>

   """
  #Branch name
  name=get_one_node(branchBlock,'h3/text()')

  #Postal address
  addrnode=get_one_branchBlock_node(branchBlock,'infoAddr')
  addr='\n'.join(addrnode.xpath('text()'))

  #Telephone
  telnode=get_one_branchBlock_node(branchBlock,'infoTel')
  tel=telnode.text

  #Email
  emailnode=get_one_branchBlock_node(branchBlock,'trackView')
  email=emailnode.text

  #Map
  mapnode=get_one_branchBlock_node(branchBlock,'viewOnMap')
  mapjs=mapnode.attrib['onclick']
  mapinfo=parse_mapjs(mapjs)

  #Combine
  d=mapinfo
  d.update({
    "branchName":name
  , "address":addr
  , "phone":tel
  , "email":email
  , "mapjs":mapjs
  })

  return d


def parse_mapjs(mapjs):
  branchId,latitude,longitude=findall('javascript:showInfoWindow\(([^,]*),([^,]*),([^,]*)',mapjs)[0]
  latitude,longitude=[float(sub('[^0-9.-]','',l)) for l in [latitude,longitude]]
  return {
    "branchId":loads(branchId)['branchId']
  , "latitude":latitude
  , "longitude":longitude
  }

def get_one_branchBlock_node(tree,classname):
  xpath='descendant::*[@class="%s"]' % classname
  return get_one_node(tree,xpath)

def get_one_node(tree,xpath):
  nodes=tree.xpath(xpath)
  assert 1==len(nodes),map(tostring,nodes)
  return nodes[0]

def request_province_list():
  return get("http://www.capitecbank.co.za/contact-us/branch-locator")

def request_province_branches(provinceId):
  return post("http://www.capitecbank.co.za/formelement.q",{
    "element":"mapcityresults"
  , "searchProvince":provinceId
  })

def load_request(r,verbose=True):
  html=r.content
  if html=="":
    print("There's nothing in the request content.")
  elif verbose:
    print(html)
  return fromstring(html)

def test_request_branch(verbose=True):
  ec_branches=request_province_branches("ec").content
  if verbose:
    request_province_branches("ec").content
  print len(ec_branches)==36504

def provinceIds():
   return [p['provinceId'] for p in get_province_list()]

def branch_response_lengths():
  for p in provinceIds():
    p_branches=request_province_branches(p).content
    print p,len(p_branches)

def branch_lists():
  for p in provinceIds():
    print(get_branch_list(p))

def extract_postcodes():
  sql = ' `rowid`, `address` from `branches`;'
  for row in select(sql):
    postcodes = findall(r'[0-9]{4}', row['address'])
    if len(postcodes) != 0:
      execute("UPDATE `branches` SET `postcode` = ? WHERE `rowid` = ? ", (postcodes[-1], row['rowid']) )
  commit()

#download()
#execute("ALTER TABLE `branches` ADD COLUMN postcode text")

extract_postcodes()from requests import post,get
from lxml.html import fromstring,tostring
from scraperwiki.sqlite import save, select, execute, commit
from scraperwiki import swimport
options=swimport('options').options
from re import findall,sub
from demjson import decode as loads
from time import time

DATE=time()

def download(verbose=True):
  provinces=get_province_list()
  if verbose:
    print("Found these provinces:")
    print(provinces)
  for province in provinces:
    if verbose:
      print("Entering this province:")
      print(province)
    branches=get_branch_list(province['provinceId'])
    if verbose:
      print("Found these branches:")
      print(branches)
    for branch in branches:
      if verbose:
        print("Entering this branch:")
        print(branch)
      branch.update(province)
    for branch in branches:
      branch['date-scraped']=DATE
    save([],branches,'branches')

def get_province_list():
  x=load_request(request_province_list())
  o=options(x.get_element_by_id("searchProvince"),ignore_text="Province",textname="provinceName",valuename="provinceId")
  return o

def get_branch_list(provinceId):
  x=load_request(request_province_branches(provinceId))
  branches=[]
  for branchBlock in x.cssselect('.branchBlock'):
    d=branchBlock_info(branchBlock)
    branches.append(d)
  return branches


def branchBlock_info(branchBlock):
  """It's one of these

      <div class="branchBlock">
        <h3>Bushbuckridge</h3>
        <p><span class="infoAddr">Shop 4<br />Bushbuckridge Shopping Centre, Bushbuckridge, 1280</span></p>
        <p><span class="infoTel">0860 10 20 43</span> <span class="infoEmail"><a href="mailto:clientcare@capitecbank.co.za" class="trackView" >clientcare@capitecbank.co.za</a></span> <span class="infoViewMap"><a href="#gmap" class="viewOnMap" onclick="javascript:showInfoWindow({ 'branchId': 74 },-24.834183,31.069195);" >View on Map</a></span></p>
      </div>

   """
  #Branch name
  name=get_one_node(branchBlock,'h3/text()')

  #Postal address
  addrnode=get_one_branchBlock_node(branchBlock,'infoAddr')
  addr='\n'.join(addrnode.xpath('text()'))

  #Telephone
  telnode=get_one_branchBlock_node(branchBlock,'infoTel')
  tel=telnode.text

  #Email
  emailnode=get_one_branchBlock_node(branchBlock,'trackView')
  email=emailnode.text

  #Map
  mapnode=get_one_branchBlock_node(branchBlock,'viewOnMap')
  mapjs=mapnode.attrib['onclick']
  mapinfo=parse_mapjs(mapjs)

  #Combine
  d=mapinfo
  d.update({
    "branchName":name
  , "address":addr
  , "phone":tel
  , "email":email
  , "mapjs":mapjs
  })

  return d


def parse_mapjs(mapjs):
  branchId,latitude,longitude=findall('javascript:showInfoWindow\(([^,]*),([^,]*),([^,]*)',mapjs)[0]
  latitude,longitude=[float(sub('[^0-9.-]','',l)) for l in [latitude,longitude]]
  return {
    "branchId":loads(branchId)['branchId']
  , "latitude":latitude
  , "longitude":longitude
  }

def get_one_branchBlock_node(tree,classname):
  xpath='descendant::*[@class="%s"]' % classname
  return get_one_node(tree,xpath)

def get_one_node(tree,xpath):
  nodes=tree.xpath(xpath)
  assert 1==len(nodes),map(tostring,nodes)
  return nodes[0]

def request_province_list():
  return get("http://www.capitecbank.co.za/contact-us/branch-locator")

def request_province_branches(provinceId):
  return post("http://www.capitecbank.co.za/formelement.q",{
    "element":"mapcityresults"
  , "searchProvince":provinceId
  })

def load_request(r,verbose=True):
  html=r.content
  if html=="":
    print("There's nothing in the request content.")
  elif verbose:
    print(html)
  return fromstring(html)

def test_request_branch(verbose=True):
  ec_branches=request_province_branches("ec").content
  if verbose:
    request_province_branches("ec").content
  print len(ec_branches)==36504

def provinceIds():
   return [p['provinceId'] for p in get_province_list()]

def branch_response_lengths():
  for p in provinceIds():
    p_branches=request_province_branches(p).content
    print p,len(p_branches)

def branch_lists():
  for p in provinceIds():
    print(get_branch_list(p))

def extract_postcodes():
  sql = ' `rowid`, `address` from `branches`;'
  for row in select(sql):
    postcodes = findall(r'[0-9]{4}', row['address'])
    if len(postcodes) != 0:
      execute("UPDATE `branches` SET `postcode` = ? WHERE `rowid` = ? ", (postcodes[-1], row['rowid']) )
  commit()

#download()
#execute("ALTER TABLE `branches` ADD COLUMN postcode text")

extract_postcodes()