from scraperwiki import swimport
from scraperwiki.sqlite import save
keyify=swimport('keyify').keyify
dsp=swimport('dsp').dsp
from time import time
strip_address = swimport('strip_address').strip_address

DOMAIN='http://www.sasfin.com'
DATE=time()

def main():
  offices=getofficelist()
  for office in offices:
    print office['path']
    d=scrapeoffice(office)
    table_name='officeinfo' if office['path']!='/CONTACT/FreightContacts.aspx' else 'freightinfo'
    save([],d,table_name)

def saveofficelist(offices):
  for row in offices:
    row['date_scraped']=DATE
    row["Physical_address"] = strip_address(row["Physical_address"])
    row["Postal_address"] = strip_address(row["Postal_address"])
  save([],offices,'urls')

def scrapeoffice(office):
  url="%s%s"%(DOMAIN,office['path'])
  xml=dsp(url,False)
  tables=xml.cssselect('.c_content table > tbody')
  assert len(tables)==1
  table=tables[0]
  nrow=int(table.xpath('count(tr)'))
  ncol=int(table.xpath('count(tr[position()=1]/td)'))

  tabnames=xml.cssselect('span.TitleHeadVIDEO')
  assert len(tabnames)==1
  d={
    "tabname":tabnames[0].text
  , "url":url
  , "date_scraped":DATE
  }

  for col in range(1,ncol+1):
    keys=table.xpath('tr[position()=1]/td[position()=%d]/text()' % col)
    assert len(keys)==1
    key=keys[0]
    value_raw=table.xpath('tr[position()>1 and position()<last()]/td[position()=%d]/text()' % col)
    value='\n'.join(value_raw).replace(u'\xa0','')

    if key!=u'\xa0':
      d[keyify(key)]=value

  return d

def getofficelist():
  offices=[{"path":'/CONTACT/HeadOffice.aspx',"name":"Head Office"}]
  xml=dsp('%s/CONTACT/HeadOffice.aspx'%DOMAIN,False)
  trs=xml.xpath('//tr[td[@class="Tabs_Selected"]/text()="Head Office"]')
  assert len(trs)==1

  a_text=trs[0].xpath('td/a/text()')
  a_href=trs[0].xpath('td/a/attribute::href')
  offices.extend(map(lambda a:{"path":a[0],"name":a[1]},zip(a_href,a_text)))
  return offices

main()from scraperwiki import swimport
from scraperwiki.sqlite import save
keyify=swimport('keyify').keyify
dsp=swimport('dsp').dsp
from time import time
strip_address = swimport('strip_address').strip_address

DOMAIN='http://www.sasfin.com'
DATE=time()

def main():
  offices=getofficelist()
  for office in offices:
    print office['path']
    d=scrapeoffice(office)
    table_name='officeinfo' if office['path']!='/CONTACT/FreightContacts.aspx' else 'freightinfo'
    save([],d,table_name)

def saveofficelist(offices):
  for row in offices:
    row['date_scraped']=DATE
    row["Physical_address"] = strip_address(row["Physical_address"])
    row["Postal_address"] = strip_address(row["Postal_address"])
  save([],offices,'urls')

def scrapeoffice(office):
  url="%s%s"%(DOMAIN,office['path'])
  xml=dsp(url,False)
  tables=xml.cssselect('.c_content table > tbody')
  assert len(tables)==1
  table=tables[0]
  nrow=int(table.xpath('count(tr)'))
  ncol=int(table.xpath('count(tr[position()=1]/td)'))

  tabnames=xml.cssselect('span.TitleHeadVIDEO')
  assert len(tabnames)==1
  d={
    "tabname":tabnames[0].text
  , "url":url
  , "date_scraped":DATE
  }

  for col in range(1,ncol+1):
    keys=table.xpath('tr[position()=1]/td[position()=%d]/text()' % col)
    assert len(keys)==1
    key=keys[0]
    value_raw=table.xpath('tr[position()>1 and position()<last()]/td[position()=%d]/text()' % col)
    value='\n'.join(value_raw).replace(u'\xa0','')

    if key!=u'\xa0':
      d[keyify(key)]=value

  return d

def getofficelist():
  offices=[{"path":'/CONTACT/HeadOffice.aspx',"name":"Head Office"}]
  xml=dsp('%s/CONTACT/HeadOffice.aspx'%DOMAIN,False)
  trs=xml.xpath('//tr[td[@class="Tabs_Selected"]/text()="Head Office"]')
  assert len(trs)==1

  a_text=trs[0].xpath('td/a/text()')
  a_href=trs[0].xpath('td/a/attribute::href')
  offices.extend(map(lambda a:{"path":a[0],"name":a[1]},zip(a_href,a_text)))
  return offices

main()