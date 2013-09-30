from scraperwiki.sqlite import save,select,show_tables
from lxml.html import fromstring
from urllib2 import Request, urlopen
from copy import copy
from time import time

def main():
  """Check what has been scraped so far, then resume.
  It might be good to check for gaps in the scraping.
  Or maybe a recursive approach isn't the best for
  search pages like this."""

  #What's already been scraped recently?
  if not 'directory' in show_tables():
    last_searched=0
  else:
    #Only skip things from the current scraper completion attempt.
    if 'scrape_completions' in show_tables():
      raw_ids=select('scrape_ids from scrape_completions order by completion_id desc limit 1')[0]['scrape_ids']
      max_to_ignore=max(map(int,raw_ids.split(',')))
      min_to_scrape=max_to_ignore+1
    else:
      min_to_scrape=1
    incomplete_scrape=select('max("search_id") as m from directory where scrape_id>='+str(min_to_scrape))[0]['m']
    if incomplete_scrape!=None:
      last_searched=incomplete_scrape
    else:
      last_searched=0

  if 'scrape_times' in show_tables():
    last_id=select('max("scrape_id") as m from scrape_times')[0]['m']
  else:
    last_id=0

  #Time of scrape start
  scrape_id=last_id+1
  save(['scrape_id'],{"scrape_id":scrape_id,"scrape_time":time()},'scrape_times')
  grab(last_searched+1,{"scrape_id":scrape_id},oncompletion=oncompletion)

def oncompletion():
  scrape_ids=[str(row['scrape_id']) for row in select('scrape_id from scrape_times')]
  if 'scrape_completions' in show_tables():
    #Increment id
    completion_id=1+select('max("completion_id") as m from scrape_completions')[0]['m']
    #Remove old scrape_ids
    completion_rows=[row['scrape_ids'] for row in select('scrape_ids from scrape_completions')]
    old_scrapes=(','.join(completion_rows)).split(',')
    for old_scrape in old_scrapes:
      scrape_ids.remove(old_scrape)
  else:
    completion_id=1
  d={
    "completion_id":completion_id
  , "scrape_ids":','.join(scrape_ids)
  }
  save(['completion_id'],d,'scrape_completions')

def _oncompletion_default():
  _print("All done")

def grab(startitem=1,extracolumns={},oncompletion=_oncompletion_default):
  #Grab
  _print('Downloading')
  xml=get_search_page(startitem)

  #Parse
  _print('Parsing')
  rows=parse(xml)

  #Add some new information
  search_id=copy(startitem)
  for row in rows:
    #Identifiers we know which items we've scraped.
    row['search_id']=search_id
    search_id=search_id+1
    #Any extra information
    row.update(extracolumns)

  #Save to the datastore
  save([],rows,'directory')

  #Recurse
  if is_last_page(xml):
    oncompletion()
  else:
    _print("Finished items "+' to '.join(map(str,current_items(xml)))+' of '+str(matched_items(xml)))
    _print("Searching for items "+str(startitem)+" to "+str(startitem+5))
    grab(startitem+5,extracolumns,oncompletion)

def parse(xml):
  """Extract structured data from the xml object"""
  table=xml.xpath('//form[@action="http://www.ccof.org/cgi-bin/organicdirectory_search.cgi"]/preceding-sibling::table[position()=1]')[0]
  trs=table.xpath('tr')
  rows=[]
  #Iterate through the five database entries
  while len(trs)>0:
    row=parse_entry(trs)
    rows.append(row)
  return rows

def parse_entry(trs):
  """Given the full list of trs, extract data from the first database entry
  and remove the first database entry from the trs."""
  d={}
  tr=trs.pop(0)
  while (not is_entry_divider(tr)) and len(trs)>0:
    pairlist=tr.xpath('descendant::*[self::font or self::a]/text()')
    if len(pairlist)!=2:
      _print("Extraction of this key-value pair was less standard.")
      _print(pairlist)
      save(['pair'],{"time":time(),"pair":'|'.join(pairlist)},'nonstandard_pairs')
    key=pairlist[0]
    value=''.join(pairlist[1:])
    d[keyify(key)]=value
    tr=trs.pop(0)
  return d

# Parse functions
def entry_dividers(xml):
  return xml.xpath('//td[@colspan="2"]/hr[@color="#006633"]')

def is_entry_divider(tr):
  """Return true if the tr divides two entries in the directory.
  An entry corresponds to a certified organic entity."""
  return 1==len(tr.xpath('td[@colspan="2"]/hr[@color="#006633"]'))


# Navigation functions
def is_last_page(xml):
  """Based on the search page, determine whether it's the last page."""
  #Get information from the page
  #matched=matched_items(xml)
  first_displayed,last_displayed=current_items(xml)
  #Check lastness
  return first_displayed>last_displayed

def matched_items(xml):
  return int(xml.xpath('//font[@color="#488050"]/b/text()')[0])

def current_items(xml):
  displayed=xml.xpath('//font[@color="#488050"]/text()')[0]
  split_on_to=displayed.split(' to ')
  first_displayed=int(split_on_to[0].split(' (')[-1])
  last_displayed=int(split_on_to[1].split(' ')[0])
  return [first_displayed,last_displayed]

def get_search_page(startitem):
  """Return the xml of a search page that contains five items,
  starting with the item corresponding to the given item number."""
  params="Business_Name=&Owner_Manager=&Address=&City=&State=&County=&Chapter=&"\
  + "Sales_Method=&Products=&IFOAM_Accredited=&checkpassword=&startitem="+str(startitem-1)
  req = Request('http://www.ccof.org/cgi-bin/organicdirectory_search.cgi', params)
  return fromstring(urlopen(req).read())

#Datastore key cleaning
def keyify(key):
  return key.replace(':','')

def _print(stuff):
  """Add verbosity for debugging."""
  pass
  #print stuff

main()from scraperwiki.sqlite import save,select,show_tables
from lxml.html import fromstring
from urllib2 import Request, urlopen
from copy import copy
from time import time

def main():
  """Check what has been scraped so far, then resume.
  It might be good to check for gaps in the scraping.
  Or maybe a recursive approach isn't the best for
  search pages like this."""

  #What's already been scraped recently?
  if not 'directory' in show_tables():
    last_searched=0
  else:
    #Only skip things from the current scraper completion attempt.
    if 'scrape_completions' in show_tables():
      raw_ids=select('scrape_ids from scrape_completions order by completion_id desc limit 1')[0]['scrape_ids']
      max_to_ignore=max(map(int,raw_ids.split(',')))
      min_to_scrape=max_to_ignore+1
    else:
      min_to_scrape=1
    incomplete_scrape=select('max("search_id") as m from directory where scrape_id>='+str(min_to_scrape))[0]['m']
    if incomplete_scrape!=None:
      last_searched=incomplete_scrape
    else:
      last_searched=0

  if 'scrape_times' in show_tables():
    last_id=select('max("scrape_id") as m from scrape_times')[0]['m']
  else:
    last_id=0

  #Time of scrape start
  scrape_id=last_id+1
  save(['scrape_id'],{"scrape_id":scrape_id,"scrape_time":time()},'scrape_times')
  grab(last_searched+1,{"scrape_id":scrape_id},oncompletion=oncompletion)

def oncompletion():
  scrape_ids=[str(row['scrape_id']) for row in select('scrape_id from scrape_times')]
  if 'scrape_completions' in show_tables():
    #Increment id
    completion_id=1+select('max("completion_id") as m from scrape_completions')[0]['m']
    #Remove old scrape_ids
    completion_rows=[row['scrape_ids'] for row in select('scrape_ids from scrape_completions')]
    old_scrapes=(','.join(completion_rows)).split(',')
    for old_scrape in old_scrapes:
      scrape_ids.remove(old_scrape)
  else:
    completion_id=1
  d={
    "completion_id":completion_id
  , "scrape_ids":','.join(scrape_ids)
  }
  save(['completion_id'],d,'scrape_completions')

def _oncompletion_default():
  _print("All done")

def grab(startitem=1,extracolumns={},oncompletion=_oncompletion_default):
  #Grab
  _print('Downloading')
  xml=get_search_page(startitem)

  #Parse
  _print('Parsing')
  rows=parse(xml)

  #Add some new information
  search_id=copy(startitem)
  for row in rows:
    #Identifiers we know which items we've scraped.
    row['search_id']=search_id
    search_id=search_id+1
    #Any extra information
    row.update(extracolumns)

  #Save to the datastore
  save([],rows,'directory')

  #Recurse
  if is_last_page(xml):
    oncompletion()
  else:
    _print("Finished items "+' to '.join(map(str,current_items(xml)))+' of '+str(matched_items(xml)))
    _print("Searching for items "+str(startitem)+" to "+str(startitem+5))
    grab(startitem+5,extracolumns,oncompletion)

def parse(xml):
  """Extract structured data from the xml object"""
  table=xml.xpath('//form[@action="http://www.ccof.org/cgi-bin/organicdirectory_search.cgi"]/preceding-sibling::table[position()=1]')[0]
  trs=table.xpath('tr')
  rows=[]
  #Iterate through the five database entries
  while len(trs)>0:
    row=parse_entry(trs)
    rows.append(row)
  return rows

def parse_entry(trs):
  """Given the full list of trs, extract data from the first database entry
  and remove the first database entry from the trs."""
  d={}
  tr=trs.pop(0)
  while (not is_entry_divider(tr)) and len(trs)>0:
    pairlist=tr.xpath('descendant::*[self::font or self::a]/text()')
    if len(pairlist)!=2:
      _print("Extraction of this key-value pair was less standard.")
      _print(pairlist)
      save(['pair'],{"time":time(),"pair":'|'.join(pairlist)},'nonstandard_pairs')
    key=pairlist[0]
    value=''.join(pairlist[1:])
    d[keyify(key)]=value
    tr=trs.pop(0)
  return d

# Parse functions
def entry_dividers(xml):
  return xml.xpath('//td[@colspan="2"]/hr[@color="#006633"]')

def is_entry_divider(tr):
  """Return true if the tr divides two entries in the directory.
  An entry corresponds to a certified organic entity."""
  return 1==len(tr.xpath('td[@colspan="2"]/hr[@color="#006633"]'))


# Navigation functions
def is_last_page(xml):
  """Based on the search page, determine whether it's the last page."""
  #Get information from the page
  #matched=matched_items(xml)
  first_displayed,last_displayed=current_items(xml)
  #Check lastness
  return first_displayed>last_displayed

def matched_items(xml):
  return int(xml.xpath('//font[@color="#488050"]/b/text()')[0])

def current_items(xml):
  displayed=xml.xpath('//font[@color="#488050"]/text()')[0]
  split_on_to=displayed.split(' to ')
  first_displayed=int(split_on_to[0].split(' (')[-1])
  last_displayed=int(split_on_to[1].split(' ')[0])
  return [first_displayed,last_displayed]

def get_search_page(startitem):
  """Return the xml of a search page that contains five items,
  starting with the item corresponding to the given item number."""
  params="Business_Name=&Owner_Manager=&Address=&City=&State=&County=&Chapter=&"\
  + "Sales_Method=&Products=&IFOAM_Accredited=&checkpassword=&startitem="+str(startitem-1)
  req = Request('http://www.ccof.org/cgi-bin/organicdirectory_search.cgi', params)
  return fromstring(urlopen(req).read())

#Datastore key cleaning
def keyify(key):
  return key.replace(':','')

def _print(stuff):
  """Add verbosity for debugging."""
  pass
  #print stuff

main()