from scraperwiki import swimport
from scraperwiki.sqlite import save
keyify=swimport('keyify').keyify
dsp=swimport('dsp').dsp
from time import time
from copy import copy
DATE=time()
strip_address = swimport('strip_address').strip_address

URLBASE="http://www.marang.co.za/"
class ParseError(Exception):
  pass

#Main controls
def main():
  links=get_links()
  for path in links:
    #Select only the interesting ones
    #And something's wrong with the history page.
    if "-" in path and path!='marang-history.asp':
      url='%s%s'%(URLBASE,path)
      print "Downloading %s" % url
      xml=dsp(url,False)

      if path=="branch-regional.asp":
        parse_regional_offices(xml,url)
      elif path=="marang-map.asp":
        parse_map(xml)
      elif path[0:6]=="branch":
        try:
          parse_branch(xml,url,path)
        except ParseError:
          print 'Error on %s' % url
          raise

def get_links():
  xml=dsp('%sbranch-regional.asp'%URLBASE,False)
  return xml.xpath('//a/attribute::href')



#Page-specific parsing
def parse_branch(xml,url,region):

  #Get table
  max_trs=max([table.xpath('count(tr)') for table in xml.xpath('//table')])
  table_nodes=xml.xpath('//table[count(tr)=%d]'%max_trs)

  #Check
  l=len(table_nodes)
  if l!=1:
    raise ParseError("I could not identify the appropriate table; %d candidates were found." % l)
  else:
    table=table_nodes[0]

  #Parse
  #from lxml.html import tostring
  #print tostring(table)
  d=parse_branch_table(table)
  d=parse_branch_table_strings(d)
  for row in d:
    row['date_scraped']=DATE
    row['region']=region
    row['url']=url
    row['full-address'] = strip_address(row['full-address'])
    row['street-address'] = strip_address(row['street-address'])
  #print [row.keys() for row in d]
  save([],d,'branches')

def parse_branch_table(table):
  d=[]
  for tr in table.xpath('tr[position()>1]'):
    addressnode,keynode,valuenode=tr.xpath('td')

    keys=[keyify(k.strip()) for k in keynode.xpath('div/p/text()')+keynode.xpath('div/p/p/text()')]
    values=[v.strip() for v in valuenode.xpath('div/p/span/text()')+valuenode.xpath('div/p/span/*[self::a or self::p]/text()')]
    if len(values)==0:
      values=[v.strip() for v in valuenode.xpath('div/p/text()')+valuenode.xpath('div/p/*[self::a or self::p]/text()')]

    for l in [keys,values]:
      if '' in l:
        l.remove('')
    assert len(keys)==len(values),(keys,values)

    row_raw=dict(zip(keys,values))
    row=copy(row_raw)

    if row_raw.has_key('ContactL'):
      row['Email']=row_raw['ContactL']
      del(row['ContactL'])

    if (row.has_key('Contact') and row.has_key('Email')) and ('@' in row_raw['Contact'] and '@' not in row_raw['Email']):
      row['Email']=row_raw['Contact']
      row['Contact']=row_raw['Email']
    row['full-address']=addressnode.text_content()

    d.append(row)
  return d

def parse_branch_table_strings(d):
  for row in d:
    if row.has_key(''):
      del(row[''])
    if row.has_key(u'\xa0'):
      del(row[u'\xa0'])
    try:
      row['postal-code']=str(int(row['full-address'].split('\n')[-1]))
    except ValueError:
      row['street-address']=row['full-address']
      row['postal-code']=''
    else:
      row['street-address']='\n'.join(row['full-address'].split('\n')[0:-1])
  return d

def parse_map(xml):
  pass

def parse_regional_offices(xml,url):
  #Get table
  table_nodes=xml.xpath('//table[@width="690"]')
  l=len(table_nodes)
  if l!=1:
    raise ParseError("I could not identify the appropriate table; %d candidates were found." % l)
  else:
    #Parse
    d=parse_regional_offices_table(table_nodes[0])

    #Save
    for row in d:
      row['date_scraped']=DATE
      row['url']=url
      row['Address'] = strip_address(row['Address'])
    save([],d,'regional_offices')




#Helpers
def parse_regional_offices_table(table):
  keys=table.xpath('tr[position()=1]/td/strong/text()')
  l=len(keys)
  if l!=4:
    raise ParseError("The wrong number of table column names was found; %d were found." % l)

  keys=[keyify(key) for key in keys]
  trs=table.xpath('tr[position()>1]')
  d=[parse_regional_offices_tr(keys,tr) for tr in trs]
  return d

def parse_regional_offices_tr(keys,tr):
  """
                  <td height="115" align="left" valign="top" class="style100">Mpumalanga
Regional Office</td>
                  <td align="left" valign="top" class="style99">&nbsp;</td>
                  <td align="left" valign="top" class="style99">013 737 6723</td>
                  <td align="left" valign="top" class="style99">Shop No. 27
                    <br>
                    Bluehaze Centre
                    <br>
                    Hazyview
                    <br>
                  (Next to Protea Tyres)&nbsp;</td>
                </tr>
"""
  values=['\n'.join(td.xpath('text()')) for td in tr.xpath('td')]
  return dict(zip(keys,values))


#Go
main()
#xml=dsp('http://www.marang.co.za/branch-limpopo.asp',save=False)
#parse_branch(xml)