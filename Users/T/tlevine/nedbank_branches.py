"Because this website's data span many pages, this scraper needs to be run about nine times to make a full scrape."

from lxml.html import fromstring
#from lxml.etree import fromstring
from time import time
import requests
from scraperwiki.sqlite import save,save_var,get_var,show_tables,select,commit,execute
from scraperwiki import swimport
options=swimport('options').options
keyify=swimport('keyify').keyify
from json import loads,dumps
strip_address = swimport('strip_address').strip_address

URLS={
  "main":"http://www.nedbank.co.za/website/content/map/branches.asp"
, "suburbs-base":"http://www.nedbank.co.za/website/content/map/getSuburbs.asp?q="
, "cities-base":"http://www.nedbank.co.za/website/content/map/getData.asp?q="
}

def main():
  if get_var('province')=='step2':
    separate_addresses()
    execute('DELETE FROM swvariables WHERE name = "province"')
    commit()
    print("""
    ================================
    This run is finished!
    ================================
    """)
  else:
    download()

class AddressError(Exception):
  pass

def separate_addresses():
  execute('DROP TABLE IF EXISTS final')
  commit()
  d=select('* from `initial`')
  for row in d:
    splitaddress=row['address'].split('\n')
    l=len(splitaddress)
    if l==3:
      row['street-address'],row['subtown'],row['town2']=splitaddress
    elif l==2:
      row['street-address'],row['subtown']=splitaddress
    else:
      raise AddressError
    row['street-address'] = row['street-address'].strip()
    row['address'] = strip_address(row['address'])
  save([],d,'final')


def download(abridge=False):
  d=[]

  #Resume the saved provinces
  provinces=getprovinces()
  province=get_var('province', provinces[0])

  #Put the date in. This will get passed along, so this is the only time I add it.
  province['date_scraped']=get_var('DATE', int(time()))

  #Get the cities
  cities=getcities(province['provinceId'])

  for city in cities:
    #Pass along the province
    city.update(province)

    branches=getbranches_with_info(city['cityId'])
    for branch in branches:
      #print branch
      branch.update(city)
      d.append(branch)

    if abridge:
      break

  i=provinces.index(province)+1
  print provinces
  if i<len(provinces):
    save_var('province',dumps(provinces[i]))
    print('Finished with branches in %s' % province['provinceName'])
  else:
    save_var('province',None)
    print('Finished with all the downloading!')

  save([],d,'initial')

def getprovinces():
  r=requests.get(URLS['main'])
  x=fromstring(r.content)

  provinces=options(x.xpath('id("province")')[0],valuename="provinceId",textname="provinceName",ignore_value="0")

  return provinces

def getcities(provinceId):
  r=requests.get("%s%s" % (URLS['suburbs-base'],provinceId))
  x=fromstring(r.content)

  citiesParent=x.xpath('//select') #This should actually have an option child, but lxml fixes the wrong html
  assert len(citiesParent)==1

  cities=options(citiesParent[0],valuename="cityId",textname="cityName",ignore_value="0")
  return cities

def getbranches_with_info(cityId):
  url="%s%s" % (URLS['cities-base'],cityId)
  r=requests.get(url)
  x=fromstring(r.content.replace('\n','').replace('\r','').replace('\t',''))
  tds=x.xpath('//td[a]')
  branches=[branchinfo(td) for td in tds]
  for branch in branches:
    branch['url']=url
  return branches

def branchinfo(td):
  keys=[keyify(key) for key in td.xpath('strong/text()')]
  l=len(keys)

  values=td.xpath('text()[position()>="%d"]' % l)
  address='\n'.join(td.xpath('text()[position()<"%d"]' % l))

  branch=dict(zip(keys,values))
  branch['address']=address

  maphref=td.xpath('a/attribute::href')[0]
  branch.update(parse_maphref(maphref))

  return branch

def parse_maphref(maphref):
  html=maphref.split("'")[1].replace('<br>','')
  x=fromstring(html)
  keys=["map_%s" % keyify(key) for key in x.xpath('strong/text()')]
  values=x.xpath('text()')
  return dict(zip(keys,values))

def test():
  assert getbranches_with_info('6855')==[{'Fax_No': ' 047 577 4110', 'url': 'http://www.nedbank.co.za/website/content/map/getData.asp?q=6855', 'map_Latitude_': u'S 31\xb0 58\u2019 3"', 'map_Longitude_': u'E 28\xb0 41\u2019 5"', 'Branch_Code': ' 178505', 'address': '    Boxer Elliodale, 17 Main Rd\n    Elliotdale\n    Elliotdale', 'Tel_No': ' 047 577 4100', 'map_Address_': ' Boxer Elliodale, 17 Main Rd', 'Email': '  '}]
  assert getcities('701')==[{'cityId': '6620', 'cityName': 'Burgersfort'}, {'cityId': '6621', 'cityName': 'Bushbuckridge'}, {'cityId': '6622', 'cityName': 'Dennilton'}, {'cityId': '6623', 'cityName': 'Driekop'}, {'cityId': '6624', 'cityName': 'Emalahleni'}, {'cityId': '6625', 'cityName': 'Ermelo'}, {'cityId': '6858', 'cityName': 'Ermelo Nu'}, {'cityId': '6626', 'cityName': 'Groblersdal'}, {'cityId': '6627', 'cityName': 'Hazyview'}, {'cityId': '6628', 'cityName': 'Malelane'}, {'cityId': '6880', 'cityName': 'Mapulaneng Nu'}, {'cityId': '6629', 'cityName': 'Middelburg'}, {'cityId': '6630', 'cityName': 'Mkobola'}, {'cityId': '6631', 'cityName': 'Nelspruit'}, {'cityId': '6895', 'cityName': 'Nkomazi Nu'}, {'cityId': '6898', 'cityName': 'Nsikazi Nu'}, {'cityId': '6632', 'cityName': 'Piet Retief'}, {'cityId': '6633', 'cityName': 'Pongola'}, {'cityId': '6634', 'cityName': 'Schoemansdal'}, {'cityId': '6635', 'cityName': 'Secunda'}, {'cityId': '6636', 'cityName': 'Standerton'}, {'cityId': '6637', 'cityName': 'White River'}, {'cityId': '6638', 'cityName': 'Witbank'}, {'cityId': '6915', 'cityName': 'Witbank Nu'}, {'cityId': '6916', 'cityName': 'Witrivier Nu'}]
  assert getprovinces()==[{'provinceName': 'Eastern Cape', 'provinceId': '696'}, {'provinceName': 'Free State', 'provinceId': '697'}, {'provinceName': 'Gauteng', 'provinceId': '698'}, {'provinceName': 'Kwazulu Natal', 'provinceId': '699'}, {'provinceName': 'Limpopo', 'provinceId': '700'}, {'provinceName': 'Mpumalanga', 'provinceId': '701'}, {'provinceName': 'North West', 'provinceId': '702'}, {'provinceName': 'Northern Cape', 'provinceId': '703'}, {'provinceName': 'Western Cape', 'provinceId': '704'}]
  assert parse_maphref("""javascript:codeLatLng(-31.96754,28.684745,'<strong>Address: </strong> Boxer Elliodale, 17 Main Rd<br><br><strong>Latitude: </strong>S 31&deg; 58&#8217; 3&quot;<br><br><strong>Longitude: </strong>E 28&deg; 41&#8217; 5&quot;');reset();""")=={'map_Latitude_': u'S 31\xb0 58\u2019 3"', 'map_Address_': ' Boxer Elliodale, 17 Main Rd', 'map_Longitude_': u'E 28\xb0 41\u2019 5"'}

#We can't really use pyunit, so let's just use this instead.
#test()

#download(abridge=True)
#separate_addresses()
#main()"Because this website's data span many pages, this scraper needs to be run about nine times to make a full scrape."

from lxml.html import fromstring
#from lxml.etree import fromstring
from time import time
import requests
from scraperwiki.sqlite import save,save_var,get_var,show_tables,select,commit,execute
from scraperwiki import swimport
options=swimport('options').options
keyify=swimport('keyify').keyify
from json import loads,dumps
strip_address = swimport('strip_address').strip_address

URLS={
  "main":"http://www.nedbank.co.za/website/content/map/branches.asp"
, "suburbs-base":"http://www.nedbank.co.za/website/content/map/getSuburbs.asp?q="
, "cities-base":"http://www.nedbank.co.za/website/content/map/getData.asp?q="
}

def main():
  if get_var('province')=='step2':
    separate_addresses()
    execute('DELETE FROM swvariables WHERE name = "province"')
    commit()
    print("""
    ================================
    This run is finished!
    ================================
    """)
  else:
    download()

class AddressError(Exception):
  pass

def separate_addresses():
  execute('DROP TABLE IF EXISTS final')
  commit()
  d=select('* from `initial`')
  for row in d:
    splitaddress=row['address'].split('\n')
    l=len(splitaddress)
    if l==3:
      row['street-address'],row['subtown'],row['town2']=splitaddress
    elif l==2:
      row['street-address'],row['subtown']=splitaddress
    else:
      raise AddressError
    row['street-address'] = row['street-address'].strip()
    row['address'] = strip_address(row['address'])
  save([],d,'final')


def download(abridge=False):
  d=[]

  #Resume the saved provinces
  provinces=getprovinces()
  province=get_var('province', provinces[0])

  #Put the date in. This will get passed along, so this is the only time I add it.
  province['date_scraped']=get_var('DATE', int(time()))

  #Get the cities
  cities=getcities(province['provinceId'])

  for city in cities:
    #Pass along the province
    city.update(province)

    branches=getbranches_with_info(city['cityId'])
    for branch in branches:
      #print branch
      branch.update(city)
      d.append(branch)

    if abridge:
      break

  i=provinces.index(province)+1
  print provinces
  if i<len(provinces):
    save_var('province',dumps(provinces[i]))
    print('Finished with branches in %s' % province['provinceName'])
  else:
    save_var('province',None)
    print('Finished with all the downloading!')

  save([],d,'initial')

def getprovinces():
  r=requests.get(URLS['main'])
  x=fromstring(r.content)

  provinces=options(x.xpath('id("province")')[0],valuename="provinceId",textname="provinceName",ignore_value="0")

  return provinces

def getcities(provinceId):
  r=requests.get("%s%s" % (URLS['suburbs-base'],provinceId))
  x=fromstring(r.content)

  citiesParent=x.xpath('//select') #This should actually have an option child, but lxml fixes the wrong html
  assert len(citiesParent)==1

  cities=options(citiesParent[0],valuename="cityId",textname="cityName",ignore_value="0")
  return cities

def getbranches_with_info(cityId):
  url="%s%s" % (URLS['cities-base'],cityId)
  r=requests.get(url)
  x=fromstring(r.content.replace('\n','').replace('\r','').replace('\t',''))
  tds=x.xpath('//td[a]')
  branches=[branchinfo(td) for td in tds]
  for branch in branches:
    branch['url']=url
  return branches

def branchinfo(td):
  keys=[keyify(key) for key in td.xpath('strong/text()')]
  l=len(keys)

  values=td.xpath('text()[position()>="%d"]' % l)
  address='\n'.join(td.xpath('text()[position()<"%d"]' % l))

  branch=dict(zip(keys,values))
  branch['address']=address

  maphref=td.xpath('a/attribute::href')[0]
  branch.update(parse_maphref(maphref))

  return branch

def parse_maphref(maphref):
  html=maphref.split("'")[1].replace('<br>','')
  x=fromstring(html)
  keys=["map_%s" % keyify(key) for key in x.xpath('strong/text()')]
  values=x.xpath('text()')
  return dict(zip(keys,values))

def test():
  assert getbranches_with_info('6855')==[{'Fax_No': ' 047 577 4110', 'url': 'http://www.nedbank.co.za/website/content/map/getData.asp?q=6855', 'map_Latitude_': u'S 31\xb0 58\u2019 3"', 'map_Longitude_': u'E 28\xb0 41\u2019 5"', 'Branch_Code': ' 178505', 'address': '    Boxer Elliodale, 17 Main Rd\n    Elliotdale\n    Elliotdale', 'Tel_No': ' 047 577 4100', 'map_Address_': ' Boxer Elliodale, 17 Main Rd', 'Email': '  '}]
  assert getcities('701')==[{'cityId': '6620', 'cityName': 'Burgersfort'}, {'cityId': '6621', 'cityName': 'Bushbuckridge'}, {'cityId': '6622', 'cityName': 'Dennilton'}, {'cityId': '6623', 'cityName': 'Driekop'}, {'cityId': '6624', 'cityName': 'Emalahleni'}, {'cityId': '6625', 'cityName': 'Ermelo'}, {'cityId': '6858', 'cityName': 'Ermelo Nu'}, {'cityId': '6626', 'cityName': 'Groblersdal'}, {'cityId': '6627', 'cityName': 'Hazyview'}, {'cityId': '6628', 'cityName': 'Malelane'}, {'cityId': '6880', 'cityName': 'Mapulaneng Nu'}, {'cityId': '6629', 'cityName': 'Middelburg'}, {'cityId': '6630', 'cityName': 'Mkobola'}, {'cityId': '6631', 'cityName': 'Nelspruit'}, {'cityId': '6895', 'cityName': 'Nkomazi Nu'}, {'cityId': '6898', 'cityName': 'Nsikazi Nu'}, {'cityId': '6632', 'cityName': 'Piet Retief'}, {'cityId': '6633', 'cityName': 'Pongola'}, {'cityId': '6634', 'cityName': 'Schoemansdal'}, {'cityId': '6635', 'cityName': 'Secunda'}, {'cityId': '6636', 'cityName': 'Standerton'}, {'cityId': '6637', 'cityName': 'White River'}, {'cityId': '6638', 'cityName': 'Witbank'}, {'cityId': '6915', 'cityName': 'Witbank Nu'}, {'cityId': '6916', 'cityName': 'Witrivier Nu'}]
  assert getprovinces()==[{'provinceName': 'Eastern Cape', 'provinceId': '696'}, {'provinceName': 'Free State', 'provinceId': '697'}, {'provinceName': 'Gauteng', 'provinceId': '698'}, {'provinceName': 'Kwazulu Natal', 'provinceId': '699'}, {'provinceName': 'Limpopo', 'provinceId': '700'}, {'provinceName': 'Mpumalanga', 'provinceId': '701'}, {'provinceName': 'North West', 'provinceId': '702'}, {'provinceName': 'Northern Cape', 'provinceId': '703'}, {'provinceName': 'Western Cape', 'provinceId': '704'}]
  assert parse_maphref("""javascript:codeLatLng(-31.96754,28.684745,'<strong>Address: </strong> Boxer Elliodale, 17 Main Rd<br><br><strong>Latitude: </strong>S 31&deg; 58&#8217; 3&quot;<br><br><strong>Longitude: </strong>E 28&deg; 41&#8217; 5&quot;');reset();""")=={'map_Latitude_': u'S 31\xb0 58\u2019 3"', 'map_Address_': ' Boxer Elliodale, 17 Main Rd', 'map_Longitude_': u'E 28\xb0 41\u2019 5"'}

#We can't really use pyunit, so let's just use this instead.
#test()

#download(abridge=True)
#separate_addresses()
#main()