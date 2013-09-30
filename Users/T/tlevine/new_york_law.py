from urllib2 import urlopen, HTTPError
from lxml.html import fromstring
from time import sleep,time

from scraperwiki.sqlite import save,select,show_tables, get_var, save_var
from scraperwiki.sqlite import execute, commit

from demjson import decode

INTERVAL=0

#Table names
OBS='observations'
META='meta'

class ServerDiedAgain(Exception):
  pass

class UnexpectedQueryResultLength(Exception):
  pass

def main():
  try:
    resume()
    search_directory_tree(nextid())
  except ServerDiedAgain:
    print "The server died again."

def save_state(js,level):
  """Save the second-to-next directory to be searched."""
  save_var(str(level),js)

def resume(levels=(4,3,2,1)):
  """Resume an incomplete scrape."""
  for level in levels:
    js=get_var(str(level))
    if js!=None:
      resume_siblings(js,level)

def resume_siblings(js,level):
  if level==1:
    print "Finished resuming"
  elif not OBS in show_tables():
    pass
  else:
    parent=select('parentjs from %s order by date_scraped desc limit 1' % OBS)[0]['parentjs']
    foo,bar,baz=(eval(parent.replace('getlaw','')))
    xml=fromstring(getlaw(foo,bar,baz))
    links=get_law_links(xml,parent)
    linkslist=[link['observation']['js'] for link in links]
    if not js in linkslist:
      #It looks like the last sibling scraped was the last child of its parent;
      #None of its siblings need to be scraped
      pass
    else:
      first=linkslist.index(js)+1
      last=len(linkslist)
      print level,first,last
      if first<last:
        for link in linkslist[first:last]:
          search_directory_tree(link,level)

def search_directory_tree(id,js='getlaw("LAWS","","MAIN")',level=1):
  try:
    sleep(INTERVAL)
#    print 'Searching for %s on level %d' % (js,level)
    save_if_menu(id,js)
    foo,bar,baz=(eval(js.replace('getlaw','')))
    raw=getlaw(foo,bar,baz)
    xml=fromstring(raw)
    links=get_law_links(xml,js)
    if 0==len(links):
      #If there aren't any links, we've reached the lowest level
      save_raw_text(id,raw,time())
      save_law_text(id,xml,time())
      save_state(js,level)
    else:
      #If there are links, save them and descend into them in a depth-first fashion
      #There will only be five levels of recursion, so this is okay for Python even though it doesn't support TRE
      for link in links:
        link['observation']['parentjs']=parentjs
        link['observation']['level']=level
      save(['id'],[link['meta'] for link in links],META)
      save(['id'],[link['observation'] for link in links],OBS)
      save_state(js,level)
      for link in links:
        nextpage=link['observation']['js']
        search_directory_tree(nextid(),nextpage,level+1)
  except:
    log_error(js=js)
    raise

def link_row(id,a,name):
  meta={
    "id":id
  , "code":a.text
  , "name":name
  }
  observation={
    "id":id
  , "js":a.attrib['href'].replace('javascript:','')
  , "date_scraped":time()
  }
  return {
    "meta":meta
  , "observation":observation
  }

def save_if_menu(id,js):
  if js=='getlaw("LAWS","","MAIN")':
    save(['id'],{
      "id":id
    , "code":"root"
    , "name":"Laws Menu"
    },'meta')
    save(['id'],{
      "id":id
    , "js":js
    , "date_scraped":time()
    },'observations')


def save_law_text(id,xml,date_scraped):
  textList=xml.xpath('//pre/text()')
  if len(textList)==0:
    textList=lawtext_expired(xml)
  text='\n'.join(textList)
  d={
    "id":id
  , "text":text
  , "date_scraped":date_scraped
  }
  save([],d,'law_raw')

def save_raw_text(id,raw,date_scraped):
  d={
    "id":id
  , "rawtext":raw
  , "date_scraped":date_scraped
  }
  save(['id'],d,'law_text')

def get_law_links(xml,parentjs):
  if is_law_menu(xml):
    links=get_law_links_frommenu(xml,nextid())
  else:
    links=get_law_links_notmenu(xml,nextid())
  return links

def get_law_links_frommenu(xml,startid):
  td_nodes=xml.xpath('id("container")/table/descendant::td[a]')
  links=[]
  id=startid
  for td in td_nodes:
    id=id+1
    a=td.xpath('a')[0]
    name=td.xpath('following-sibling::td[position()=1]/text()')[0]
    links.append(link_row(id,a,name))
  return links

def get_law_links_notmenu(xml,startid):
  a_nodes=xml.xpath('id("container")/descendant::a')
  links=[]
  id=startid
  for a in a_nodes:
    id=id+1
    name=a.xpath('following-sibling::text()[position()=1]')[0]
    links.append(link_row(id,a,name))
  return links

def is_law_menu(xml):
  """Check whether the current page is the top menu page.
  That page is formatted differently from the others.
  This function looks for a link to the menu page;
  this link is not on the menu page."""
  return 0==len(xml.xpath('//a[@href=\'JAVASCRIPT:getlaw("LAWS","","MAIN")\']'))

def getlaw(CGI,QDATA,LIST):
  """Replacement for the Javascript function.
  CGI isn't used at all, and LIST is hardly used."""
  QDATA=QDATA.replace(' ','%20')
  url='http://public.leginfo.state.ny.us/LAWSSEAF.cgi?QUERYTYPE=LAWS+&QUERYDATA=%s+&LIST=%s+' % (QDATA,LIST)
  try:
    r=urlopen(url)
  except HTTPError:
    raise ServerDiedAgain
  else:
    return r.read()

def getlawq(QDATA):
  """getlaw without the unnecessary parameters"""
  return getlaw('',QDATA,'')

def lawtext_expired(xml):
  return xml.xpath('id("container")/text()')[0]

def log_error(js=None,id=None):
  """Log errors."""
  d={"id":id,"js":js,"date":time()}
  save([],d,'errors')

def nextid():
  defaultquery=[{"id":0}]
  if not OBS in show_tables():
    idquery=defaultquery
  else:
    idquery=select('max(id) as id from %s' % OBS)
    if len(idquery)==0:
      idquery=defaultquery
  id=idquery[0]['id']
  return id

#main()from urllib2 import urlopen, HTTPError
from lxml.html import fromstring
from time import sleep,time

from scraperwiki.sqlite import save,select,show_tables, get_var, save_var
from scraperwiki.sqlite import execute, commit

from demjson import decode

INTERVAL=0

#Table names
OBS='observations'
META='meta'

class ServerDiedAgain(Exception):
  pass

class UnexpectedQueryResultLength(Exception):
  pass

def main():
  try:
    resume()
    search_directory_tree(nextid())
  except ServerDiedAgain:
    print "The server died again."

def save_state(js,level):
  """Save the second-to-next directory to be searched."""
  save_var(str(level),js)

def resume(levels=(4,3,2,1)):
  """Resume an incomplete scrape."""
  for level in levels:
    js=get_var(str(level))
    if js!=None:
      resume_siblings(js,level)

def resume_siblings(js,level):
  if level==1:
    print "Finished resuming"
  elif not OBS in show_tables():
    pass
  else:
    parent=select('parentjs from %s order by date_scraped desc limit 1' % OBS)[0]['parentjs']
    foo,bar,baz=(eval(parent.replace('getlaw','')))
    xml=fromstring(getlaw(foo,bar,baz))
    links=get_law_links(xml,parent)
    linkslist=[link['observation']['js'] for link in links]
    if not js in linkslist:
      #It looks like the last sibling scraped was the last child of its parent;
      #None of its siblings need to be scraped
      pass
    else:
      first=linkslist.index(js)+1
      last=len(linkslist)
      print level,first,last
      if first<last:
        for link in linkslist[first:last]:
          search_directory_tree(link,level)

def search_directory_tree(id,js='getlaw("LAWS","","MAIN")',level=1):
  try:
    sleep(INTERVAL)
#    print 'Searching for %s on level %d' % (js,level)
    save_if_menu(id,js)
    foo,bar,baz=(eval(js.replace('getlaw','')))
    raw=getlaw(foo,bar,baz)
    xml=fromstring(raw)
    links=get_law_links(xml,js)
    if 0==len(links):
      #If there aren't any links, we've reached the lowest level
      save_raw_text(id,raw,time())
      save_law_text(id,xml,time())
      save_state(js,level)
    else:
      #If there are links, save them and descend into them in a depth-first fashion
      #There will only be five levels of recursion, so this is okay for Python even though it doesn't support TRE
      for link in links:
        link['observation']['parentjs']=parentjs
        link['observation']['level']=level
      save(['id'],[link['meta'] for link in links],META)
      save(['id'],[link['observation'] for link in links],OBS)
      save_state(js,level)
      for link in links:
        nextpage=link['observation']['js']
        search_directory_tree(nextid(),nextpage,level+1)
  except:
    log_error(js=js)
    raise

def link_row(id,a,name):
  meta={
    "id":id
  , "code":a.text
  , "name":name
  }
  observation={
    "id":id
  , "js":a.attrib['href'].replace('javascript:','')
  , "date_scraped":time()
  }
  return {
    "meta":meta
  , "observation":observation
  }

def save_if_menu(id,js):
  if js=='getlaw("LAWS","","MAIN")':
    save(['id'],{
      "id":id
    , "code":"root"
    , "name":"Laws Menu"
    },'meta')
    save(['id'],{
      "id":id
    , "js":js
    , "date_scraped":time()
    },'observations')


def save_law_text(id,xml,date_scraped):
  textList=xml.xpath('//pre/text()')
  if len(textList)==0:
    textList=lawtext_expired(xml)
  text='\n'.join(textList)
  d={
    "id":id
  , "text":text
  , "date_scraped":date_scraped
  }
  save([],d,'law_raw')

def save_raw_text(id,raw,date_scraped):
  d={
    "id":id
  , "rawtext":raw
  , "date_scraped":date_scraped
  }
  save(['id'],d,'law_text')

def get_law_links(xml,parentjs):
  if is_law_menu(xml):
    links=get_law_links_frommenu(xml,nextid())
  else:
    links=get_law_links_notmenu(xml,nextid())
  return links

def get_law_links_frommenu(xml,startid):
  td_nodes=xml.xpath('id("container")/table/descendant::td[a]')
  links=[]
  id=startid
  for td in td_nodes:
    id=id+1
    a=td.xpath('a')[0]
    name=td.xpath('following-sibling::td[position()=1]/text()')[0]
    links.append(link_row(id,a,name))
  return links

def get_law_links_notmenu(xml,startid):
  a_nodes=xml.xpath('id("container")/descendant::a')
  links=[]
  id=startid
  for a in a_nodes:
    id=id+1
    name=a.xpath('following-sibling::text()[position()=1]')[0]
    links.append(link_row(id,a,name))
  return links

def is_law_menu(xml):
  """Check whether the current page is the top menu page.
  That page is formatted differently from the others.
  This function looks for a link to the menu page;
  this link is not on the menu page."""
  return 0==len(xml.xpath('//a[@href=\'JAVASCRIPT:getlaw("LAWS","","MAIN")\']'))

def getlaw(CGI,QDATA,LIST):
  """Replacement for the Javascript function.
  CGI isn't used at all, and LIST is hardly used."""
  QDATA=QDATA.replace(' ','%20')
  url='http://public.leginfo.state.ny.us/LAWSSEAF.cgi?QUERYTYPE=LAWS+&QUERYDATA=%s+&LIST=%s+' % (QDATA,LIST)
  try:
    r=urlopen(url)
  except HTTPError:
    raise ServerDiedAgain
  else:
    return r.read()

def getlawq(QDATA):
  """getlaw without the unnecessary parameters"""
  return getlaw('',QDATA,'')

def lawtext_expired(xml):
  return xml.xpath('id("container")/text()')[0]

def log_error(js=None,id=None):
  """Log errors."""
  d={"id":id,"js":js,"date":time()}
  save([],d,'errors')

def nextid():
  defaultquery=[{"id":0}]
  if not OBS in show_tables():
    idquery=defaultquery
  else:
    idquery=select('max(id) as id from %s' % OBS)
    if len(idquery)==0:
      idquery=defaultquery
  id=idquery[0]['id']
  return id

#main()