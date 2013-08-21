from scraperwiki import swimport
dsp=swimport('dsp').dsp
import re
from time import time
from scraperwiki.sqlite import save
strip_address = swimport('strip_address').strip_address

DATE=time()

URLS={
  "dir":"http://www.gbsbank.co.za/LocationList.aspx"
, "domain":"http://www.gbsbank.co.za/"
, "office-base-rel":"Location.aspx?type="
}

def main():
  d=[]
  for href in get_office_type_hrefs():
    d.extend(get_office_info(href))
  for row in d:
    row['date_scraped']=DATE
  save([],d,'final')


# -------------------------------------------------------

def get_office_type_hrefs():
  x=dsp(URLS['dir'],False)
  hrefs=x.xpath('//a/attribute::href')
  office_hrefs=[]
  for href in hrefs:
    if URLS['office-base-rel']==href[0:-1]:
      office_hrefs.append(href)
  return office_hrefs

def get_office_info(href):
  url=URLS['domain']+href
  x=dsp(url,False)
  tables=x.xpath('//table')
  d=[]
  for table in tables:
    row=parse_office_table(table)

    #The rest of the loop is page-level information
    nodes=x.xpath('id("textholder2")/b/text()')
    assert len(nodes)==1
    row['office-type']=nodes[0]

    row['url']=url

    d.append(row)
  return d

def parse_office_table(table,verbose=True):
  row={}
  assert table.xpath('count(tr)')==table.xpath('count(tr/td)')

  #Save the raw text
  row['raw']=', '.join(table.xpath('tr/td/text()'))

  #Initialize street address
  streetAddress=[]

  #Save each line separately
  for line in table.xpath('tr/td/text()'):
    if "contact detail" in line.lower():
      row['office-name']=re.sub('contact detail.*$','',line, flags=re.IGNORECASE).strip()
    elif "@" in line:
      row['email']=line
    elif 10==len(re.sub('[^0-9]','',line)):
      row['phone']=line
    else:
      streetAddress.append(line)

  row['street-address']=', '.join(streetAddress)

  if verbose:
    print("Scraped %s contact information" % row['office-name'])

  return row

main()
