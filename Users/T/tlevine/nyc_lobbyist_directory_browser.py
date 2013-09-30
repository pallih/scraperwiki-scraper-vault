from requests import get,post
from scraperwiki import swimport
from scraperwiki.sqlite import save,show_tables,select,execute,get_var,save_var,commit
from lxml.html import fromstring
from copy import copy
import re,datetime
options=swimport('options').options
keyify=swimport('keyify').keyify

#randomsleep=swimport('randomsleep').randomsleep
from time import sleep
def randomsleep():
  "Not random"
  sleep(0.1)

CLIENT_TABLES=('clients','clients_urls','clients_lobbyists','clients_details')

URLS={
  "menu":"http://www.nyc.gov/lobbyistsearch/index.jsp"
, "form-action":"http://www.nyc.gov/lobbyistsearch/directory.jsp"
, "result-base":"http://www.nyc.gov/lobbyistsearch/"
}

MORE_QUERY_STRING={
  "lobbyist":"&op=&pg_l="
, "client":"&op=&pg_c="
, "base":"&op=&pg_"
, "re":re.compile(r"&op=&pg_[lc]=")
}

def main():
  savemenu()
  browse()
  jobs()


def main2():
  try:
    jobs(10)
  except Exception,e:
    print e

# --------------------------------------------------
# Get URLs

def browse_with_resume():
  scraper_state=get_scraper_state()
  if 0==len(scraper_state['years-to-do']):
    print("All of the alphabetical directory listings pages have already been scraped.")
  else:
    #Finish the current year
    firstyear=scraper_state['years-to-do'].pop(0)
    print("Resuming from %s" % firstyear)
    for view in scraper_state["remaining-views-this-year"]:
      browsepage(firstyear,view)
      randomsleep()

    #Remaining years
    for year in scraper_state['years-to-do']:
      print("Scraping %s" % year)
      for view in scraper_state['all-views']:
        browsepage(year,view)
        randomsleep()

def get_scraper_state():
  all_views=[row['value'] for row in select('value FROM views ORDER BY value', verbose=False)]
  if 'links' not in show_tables():
    years_to_do=[row['value'] for row in select('value FROM years ORDER BY value', verbose=False)]
    remaining_views_this_year=all_views
  else:
    finished=select('max(view) as "view",year from links where year=(select max(year) from links)', verbose=False)
    years_to_do=[row['value'] for row in select('value FROM years WHERE value>"%s" ORDER BY value' % finished[0]['year'], verbose=False)]
    remaining_views_this_year=[row['value'] for row in select('value from views where value>"%s"' % finished[0]['view'], verbose=False)]
    del(finished)
  return {
    "all-views":all_views
  , "years-to-do":years_to_do
  , "remaining-views-this-year":remaining_views_this_year
  }

browse=browse_with_resume

def savemenu():
  print("Loading the menu page and checking for years")
  m=Menu()
  save(['value'],m.getyears(),'years')
  save(['value'],m.getviews(),'views')

class Menu:
  def __init__(self):
    self.r=get(URLS['menu'])
    self.x=fromstring(self.r.content)

  def getyears(self):
    return self.getoptions('year_select')

  def getviews(self):
    return self.getoptions('view_select')

  def getoptions(self,select_name):
    nodes=self.x.xpath('//select[@name="%s"]' % select_name)
    assert len(nodes)==1,nodes
    return options(nodes[0],ignore_value='')

def browsepage(year,view,slow=True):
  """
  Browse for a particular year (like "2010") and view (like "All Clients").

  Save the following.

  {"year":"2008","view","All Lobbyists","text":"1199 SEIU United Healthcare Workers East","href":"http://www.nyc.gov/lobbyistsearch/search?lobbyist=1199+SEIU+United+Healthcare+Workers+East"}

  Save the entire page at once for simple atomicity.
  """
  params={
    "year_select":year
  , "view_select":view
  }
  r=post(URLS['form-action'],params)
  x=fromstring(r.content)
  orglinks=x.cssselect('a.backtolist')
  d=[]
  for orglink in orglinks:
    if "#"==orglink.attrib['href'][0]:
      #Link just brings you to the top of the page
      pass
    else:
      d.append({"year":year,"view":view,"name":orglink.text,"href":orglink.attrib['href']})

  save(['href'],d,'links')

# --------------------------------------------------
# Parse result pages

class ResumeError(Exception):
  pass

def atomic():
  if "client"==pagetype(get_var('previous_href')):
    table_names=CLIENT_TABLES
  elif "lobbyist"==pagetype(get_var('previous_href')):
    table_names=LOBBYIST_TABLES
  else:
    raise ResumeError('The type of the previous href, "%s", could not be determined.' % get_var('previous_href'))

  if "clients_urls" in show_tables():
    sourceUrl=select('distinct sourceUrl as "s" from `clients_urls` where jobId=(select max(jobId) from `clients_urls`)')[0]['s']
    for table_name in table_names:
      execute('DELETE FROM `%s` where jobId in (select jobId from clients_urls where sourceUrl="%s")' % (table_name,sourceUrl))
    commit()
    return sourceUrl

def drop_above_jobId(jobId,table_names):
  for table_name in table_names:
    execute('DELETE FROM `%s` where jobId>%d' % (table_name,jobId))
  commit()

def getnexthrefs(limit,previous_href):
  return [row['href'] for row in select('href FROM links WHERE href>? ORDER BY href LIMIT %d' % limit,previous_href,verbose=False)]

def jobs(limit=2):
  print("Scraping individual job information")
  previous_href=get_var('previous_href',verbose=False)

  if previous_href==None:
    hrefs=[row['href'] for row in select('href FROM links ORDER BY href LIMIT %d' % limit,verbose=False)]

  else:
    hrefs=getnexthrefs(limit,previous_href)
    previous_url=atomic()

    if MORE_QUERY_STRING['base'] in previous_url:
      print "Resuming from %s" % previous_url
      url,startpage_str=re.split(MORE_QUERY_STRING['re'],previous_url)
      href_resume=url.replace('http://www.nyc.gov/lobbyistsearch/','')
      startpage=int(startpage_str)
      paginate_result(href_resume,startpage=startpage)
      randomsleep()

  for href in hrefs:
    paginate_result(href,startpage=1)
    randomsleep()
  save_var('previous_href',hrefs[-1],verbose=False)



def paginate_result(hrefbase,startpage=1):
  finished=False
  nextpage=startpage
  while finished==False:
    href=hrefbase+MORE_QUERY_STRING[pagetype(hrefbase)]+str(nextpage)
    t=parse_result(href)

    nextpage+=1
    finished=(nextpage-1==t.lastPage())
    randomsleep()

def pagetype(href):
  return href.split('?')[1].split('=')[0]

def parse_result(href):
  """
  Determine the page type, and run the appropriate parsing function.
  Return true if it has reached the last page.
  """
  url=URLS['result-base']+href
  parse_functions={
    "lobbyist":parse_lobbyist
  , "client":parse_client
  }
  return parse_functions[pagetype(href)](url)

def parse_client(url):
  t=ClientTable(url)
  t.parse_and_save()
  return t

def parse_lobbyist(url):
  "A url like http://www.nyc.gov/lobbyistsearch/search?lobbyist=victoria+contino"
  t=LobbyistTable(url)
  t.parse_and_save()
  return t

class JobsTable:
  def __init__(self,url):
    x=fromstring(get(url).content)
    nodes=x.xpath('//table[@bgcolor="white"]')
    assert 1==len(nodes)

    self.url=url
    self.tree=nodes[0]

  def _parse_and_save(self,SpecificDataRow,maintable):
    "Clean up stuff"

    #Skip the raw parse
    #job_raw=self.rawparse()
    #for row in job_raw:
    #  row['url']=self.url
    #save([],job_raw,maintable+'raw',verbose=False)

    for tr in self.getTableRows():
      #Get the next jobId
      if maintable in show_tables():
        jobId=select('max(jobId) as "jobId" from `%s`' % maintable, verbose=False)[0]['jobId']+1
      else:
        jobId=1

      r=SpecificDataRow(tr,jobId,self.url)
      r.parse_and_save()

  def nexthref(self):
    orig=self.getPageRow().xpath('td/a/@href')[0]
    return re.sub(r'jsessionid[^?]+\?','?',orig)

  def pageNums(self):
    currentpagetext=self.getPageRow().xpath('td/text()')[0]
    foo=re.search(r'([0-9]+) of ([0-9]+)',currentpagetext)
    return map(int,[foo.group(1),foo.group(2)])

  def currentPage(self):
    return self.pageNums()[0]

  def lastPage(self):
    return self.pageNums()[1]

  def getTableRows(self):
    "Skip the empty, header and page rows"
    return self.tree.xpath('tr')[2:-1]

  def getHeaderRow(self):
    return self.tree.xpath('tr[position()=2]')[0]
  
  def getPageRow(self):
    return self.tree.xpath('tr[position()=last()]')[0]

  def getcolnames(self):
    return [keyify(td.text_content()) for td in self.getHeaderRow()]

  def rawparse(self):
    colnames=self.getcolnames()
    d=[]
    for tr in self.getTableRows():
      plaintext=[td.text_content() for td in tr.xpath('td')]
      d_row=dict(zip(colnames,plaintext))
      d.append(d_row)
    return d

class ClientTable(JobsTable):
  def parse_and_save(self):
    self._parse_and_save(ClientDataRow,'clients')

class LobbyistTable(JobsTable):
  def parse_and_save(self):
    self._parse_and_save(LobbyistDataRow,'lobbyists')

class DataRow:
  DETAIL_COLNAMES=['detailId','compensation','reimbursement']
  def __init__(self,tr,jobId,url):
    "Takes an lxml tr node"
    self.tr=tr
    self.jobId=jobId
    self.url=url

  def target_and_subject(self):
    nodes=self.tr.xpath('td[position()=last()]/div/text()')
    if 3==len(nodes):
      d={}
      d['target'],d['subject']=nodes[1:3]
    else:
      #http://www.nyc.gov/lobbyistsearch/search?client=10+Gold+L.L.C.&op=&pg_c=2
      d={
        "target":None
      , "subject":None
      }
    return d

  def parse_detail(self):
    nodes=self.tr.xpath('td[position()=last()]/div/table')
    assert 1==len(nodes),nodes
    detail_table=nodes[0]

    d=[]
    for tr in detail_table.xpath('tr[position()>1]'):
      values=[td.text_content() for td in tr.xpath('td')]
      values[0]=keyify(values[0])
      values[1:3]=map(self.money_as_float,values[1:3])
      row=dict(zip(self.DETAIL_COLNAMES,values))
      row['jobId']=self.jobId
      d.append(row)
    return d

  @staticmethod
  def money_as_float(money):
    foo=re.sub(r'[,$]','',money)
    try:
      return float(foo)
    except:
      return None

  def parse_main(self):
    "Depends on a _parse_main function defined for the specific table type"
    d=self._parse_main()
    d.update(self.target_and_subject())
    return d

  @staticmethod
  def parsedate(rawdate):
     return datetime.datetime.strptime(rawdate,'%m/%d/%Y').date()

  def get_td_text_by_position(self,position):
    return self.tr.xpath('td[position()=%d]' % int(position) )[0].text_content().strip()

  def get_td_text_nodes_by_position(self,position):
    return '\n'.join(self.tr.xpath('td[position()=%d]/text()') % int(position)).strip()

  @staticmethod
  def linklist_from_cell(td,textname="text",hrefname="href",sourcename="source",sourcevalue=None):
    "Extract a list of links from one td node"
    a_nodes=td.xpath('a')
    d=[{textname:a.text,hrefname:a.attrib['href']} for a in a_nodes]
    if sourcevalue!=None:
      for row in d:
        row[sourcename]=sourcevalue
    return d


class ClientDataRow(DataRow):
  "More parsing on a client data row"
  def parse_and_save(self):
    job=self.parse_main()
    lobbyists=self.parse_lobbyists()
    detail=self.parse_detail()

    save(['jobId'],job,'clients',verbose=False)
    save([],lobbyists,'clients_lobbyists',verbose=False)
    save([],detail,'clients_details',verbose=False)
    save(['jobId','sourceUrl'],{"jobId":self.jobId,"sourceUrl":self.url},'clients_urls')

  def parse_lobbyists(self):
    td=self.tr.xpath('td[position()=5]')[0]
    return self.linklist_from_cell(
      td
    , textname="lobbyist"
    , hrefname="lobbyist_url"
    , sourcename="jobId"
    , sourcevalue=self.jobId
    )

  def _parse_main(self):
    "Stuff that fits in one table"
    lobbyist_url_nodes=self.tr.xpath('td[position()=6]/a/@href')
    assert len(lobbyist_url_nodes)==1,lobbyist_url_nodes

    return {
      'jobId':self.jobId
    , 'client-name':self.get_td_text_by_position(1)
    , 'client-address':self.get_td_text_by_position(2)
    , 'begin-date':self.parsedate(self.get_td_text_by_position(3))
    , 'end-date':self.parsedate(self.get_td_text_by_position(4))
    , 'lobbyist-address':self.get_td_text_by_position(6)
    , 'lobbyist-url':lobbyist_url_nodes[0]
    , 'lobbyist-officer':self.get_td_text_by_position(7)
    }


class LobbyistDataRow(DataRow):
  "More parsing on a client data row"
  def parse_and_save(self):
    job=self.parse_main()
    lobbyists=self.parse_lobbyists()
    detail=self.parse_detail()

    save(['jobId'],job,'lobbyists',verbose=False)
    save([],lobbyists,'lobbyists_lobbyists',verbose=False)
    save([],detail,'lobbyists_details',verbose=False)
    save(['jobId','sourceUrl'],{"jobId":self.jobId,"sourceUrl":self.url},'lobbyists_urls')

  def parse_lobbyists(self):
    td=self.tr.xpath('td[position()=5]')[0]
    return self.linklist_from_cell(
      td
    , textname="lobbyist"
    , hrefname="lobbyist_url"
    , sourcename="jobId"
    , sourcevalue=self.jobId
    )

  def _parse_main(self):
    "Stuff that fits in one table"
    client_url_nodes=self.tr.xpath('td[position()=4]/a/@href')
    assert len(client_url_nodes)==1,lobbyist_url_nodes

    return {
      'jobId':self.jobId
    , 'lobbyist-principal':self.get_td_text_by_position(1)
    , 'lobbyist-address':self.get_td_text_by_position(2)
    , 'lobbyist-officer':self.get_td_text_by_position(3)
    , 'client-address':self.get_td_text_by_position(4)
    , 'client-url':client_url_nodes[0]
    , 'begin-date':self.parsedate(self.get_td_text_by_position(6))
    , 'end-date':self.parsedate(self.get_td_text_by_position(7))
    }



def legend():
  x=fromstring(get('http://www.nyc.gov/lobbyistsearch/helpguide.html').content)

  d=[]
  column_base={
    "name":""
  , "value":""
  }
  column=copy(column_base)
  for p in x.xpath('id("fielddesc")/../../p'):
    potential_name=''.join(p.xpath('b[span[@class="bodytext_bold_orange"]]/text()'))
    if potential_name=='' and p.text!=None:
      column['value']+=p.text+'\n'
    elif potential_name!='':
      d.append(column)
      column=copy(column_base)
      column['name']=potential_name
  return d[1:]

# --------------------------------------------------
# Go
def clear():
  execute('DROP TABLE IF EXISTS clients')
  execute('DROP TABLE IF EXISTS clientsraw')
  execute('DROP TABLE IF EXISTS clients_urls')
  execute('DROP TABLE IF EXISTS clients_lobbyists')
  execute('DROP TABLE IF EXISTS clients_details')
  execute('DROP TABLE IF EXISTS lobbyists')
  execute('DROP TABLE IF EXISTS lobbyistsraw')
  execute('DROP TABLE IF EXISTS lobbyists_urls')
  execute('DROP TABLE IF EXISTS lobbyists_lobbyists')
  execute('DROP TABLE IF EXISTS lobbyists_details')
  save_var('previous_href',None)

def demo():
  parse_result('search?client=FIFTEEN%20CENTRAL%20PARK%20WEST%20CONDOMINIUM')
  parse_result('search?lobbyist=victoria+contino')

#browsepage('2008','All Lobbyists')
#demo()

#Dunno why I needed to fix this manually...
#save_var('previous_href','search?client=104+Charlton+L+L+C')
#drop_above_jobId(21965,CLIENT_TABLES)

#save([],legend(),'legend')

main2()from requests import get,post
from scraperwiki import swimport
from scraperwiki.sqlite import save,show_tables,select,execute,get_var,save_var,commit
from lxml.html import fromstring
from copy import copy
import re,datetime
options=swimport('options').options
keyify=swimport('keyify').keyify

#randomsleep=swimport('randomsleep').randomsleep
from time import sleep
def randomsleep():
  "Not random"
  sleep(0.1)

CLIENT_TABLES=('clients','clients_urls','clients_lobbyists','clients_details')

URLS={
  "menu":"http://www.nyc.gov/lobbyistsearch/index.jsp"
, "form-action":"http://www.nyc.gov/lobbyistsearch/directory.jsp"
, "result-base":"http://www.nyc.gov/lobbyistsearch/"
}

MORE_QUERY_STRING={
  "lobbyist":"&op=&pg_l="
, "client":"&op=&pg_c="
, "base":"&op=&pg_"
, "re":re.compile(r"&op=&pg_[lc]=")
}

def main():
  savemenu()
  browse()
  jobs()


def main2():
  try:
    jobs(10)
  except Exception,e:
    print e

# --------------------------------------------------
# Get URLs

def browse_with_resume():
  scraper_state=get_scraper_state()
  if 0==len(scraper_state['years-to-do']):
    print("All of the alphabetical directory listings pages have already been scraped.")
  else:
    #Finish the current year
    firstyear=scraper_state['years-to-do'].pop(0)
    print("Resuming from %s" % firstyear)
    for view in scraper_state["remaining-views-this-year"]:
      browsepage(firstyear,view)
      randomsleep()

    #Remaining years
    for year in scraper_state['years-to-do']:
      print("Scraping %s" % year)
      for view in scraper_state['all-views']:
        browsepage(year,view)
        randomsleep()

def get_scraper_state():
  all_views=[row['value'] for row in select('value FROM views ORDER BY value', verbose=False)]
  if 'links' not in show_tables():
    years_to_do=[row['value'] for row in select('value FROM years ORDER BY value', verbose=False)]
    remaining_views_this_year=all_views
  else:
    finished=select('max(view) as "view",year from links where year=(select max(year) from links)', verbose=False)
    years_to_do=[row['value'] for row in select('value FROM years WHERE value>"%s" ORDER BY value' % finished[0]['year'], verbose=False)]
    remaining_views_this_year=[row['value'] for row in select('value from views where value>"%s"' % finished[0]['view'], verbose=False)]
    del(finished)
  return {
    "all-views":all_views
  , "years-to-do":years_to_do
  , "remaining-views-this-year":remaining_views_this_year
  }

browse=browse_with_resume

def savemenu():
  print("Loading the menu page and checking for years")
  m=Menu()
  save(['value'],m.getyears(),'years')
  save(['value'],m.getviews(),'views')

class Menu:
  def __init__(self):
    self.r=get(URLS['menu'])
    self.x=fromstring(self.r.content)

  def getyears(self):
    return self.getoptions('year_select')

  def getviews(self):
    return self.getoptions('view_select')

  def getoptions(self,select_name):
    nodes=self.x.xpath('//select[@name="%s"]' % select_name)
    assert len(nodes)==1,nodes
    return options(nodes[0],ignore_value='')

def browsepage(year,view,slow=True):
  """
  Browse for a particular year (like "2010") and view (like "All Clients").

  Save the following.

  {"year":"2008","view","All Lobbyists","text":"1199 SEIU United Healthcare Workers East","href":"http://www.nyc.gov/lobbyistsearch/search?lobbyist=1199+SEIU+United+Healthcare+Workers+East"}

  Save the entire page at once for simple atomicity.
  """
  params={
    "year_select":year
  , "view_select":view
  }
  r=post(URLS['form-action'],params)
  x=fromstring(r.content)
  orglinks=x.cssselect('a.backtolist')
  d=[]
  for orglink in orglinks:
    if "#"==orglink.attrib['href'][0]:
      #Link just brings you to the top of the page
      pass
    else:
      d.append({"year":year,"view":view,"name":orglink.text,"href":orglink.attrib['href']})

  save(['href'],d,'links')

# --------------------------------------------------
# Parse result pages

class ResumeError(Exception):
  pass

def atomic():
  if "client"==pagetype(get_var('previous_href')):
    table_names=CLIENT_TABLES
  elif "lobbyist"==pagetype(get_var('previous_href')):
    table_names=LOBBYIST_TABLES
  else:
    raise ResumeError('The type of the previous href, "%s", could not be determined.' % get_var('previous_href'))

  if "clients_urls" in show_tables():
    sourceUrl=select('distinct sourceUrl as "s" from `clients_urls` where jobId=(select max(jobId) from `clients_urls`)')[0]['s']
    for table_name in table_names:
      execute('DELETE FROM `%s` where jobId in (select jobId from clients_urls where sourceUrl="%s")' % (table_name,sourceUrl))
    commit()
    return sourceUrl

def drop_above_jobId(jobId,table_names):
  for table_name in table_names:
    execute('DELETE FROM `%s` where jobId>%d' % (table_name,jobId))
  commit()

def getnexthrefs(limit,previous_href):
  return [row['href'] for row in select('href FROM links WHERE href>? ORDER BY href LIMIT %d' % limit,previous_href,verbose=False)]

def jobs(limit=2):
  print("Scraping individual job information")
  previous_href=get_var('previous_href',verbose=False)

  if previous_href==None:
    hrefs=[row['href'] for row in select('href FROM links ORDER BY href LIMIT %d' % limit,verbose=False)]

  else:
    hrefs=getnexthrefs(limit,previous_href)
    previous_url=atomic()

    if MORE_QUERY_STRING['base'] in previous_url:
      print "Resuming from %s" % previous_url
      url,startpage_str=re.split(MORE_QUERY_STRING['re'],previous_url)
      href_resume=url.replace('http://www.nyc.gov/lobbyistsearch/','')
      startpage=int(startpage_str)
      paginate_result(href_resume,startpage=startpage)
      randomsleep()

  for href in hrefs:
    paginate_result(href,startpage=1)
    randomsleep()
  save_var('previous_href',hrefs[-1],verbose=False)



def paginate_result(hrefbase,startpage=1):
  finished=False
  nextpage=startpage
  while finished==False:
    href=hrefbase+MORE_QUERY_STRING[pagetype(hrefbase)]+str(nextpage)
    t=parse_result(href)

    nextpage+=1
    finished=(nextpage-1==t.lastPage())
    randomsleep()

def pagetype(href):
  return href.split('?')[1].split('=')[0]

def parse_result(href):
  """
  Determine the page type, and run the appropriate parsing function.
  Return true if it has reached the last page.
  """
  url=URLS['result-base']+href
  parse_functions={
    "lobbyist":parse_lobbyist
  , "client":parse_client
  }
  return parse_functions[pagetype(href)](url)

def parse_client(url):
  t=ClientTable(url)
  t.parse_and_save()
  return t

def parse_lobbyist(url):
  "A url like http://www.nyc.gov/lobbyistsearch/search?lobbyist=victoria+contino"
  t=LobbyistTable(url)
  t.parse_and_save()
  return t

class JobsTable:
  def __init__(self,url):
    x=fromstring(get(url).content)
    nodes=x.xpath('//table[@bgcolor="white"]')
    assert 1==len(nodes)

    self.url=url
    self.tree=nodes[0]

  def _parse_and_save(self,SpecificDataRow,maintable):
    "Clean up stuff"

    #Skip the raw parse
    #job_raw=self.rawparse()
    #for row in job_raw:
    #  row['url']=self.url
    #save([],job_raw,maintable+'raw',verbose=False)

    for tr in self.getTableRows():
      #Get the next jobId
      if maintable in show_tables():
        jobId=select('max(jobId) as "jobId" from `%s`' % maintable, verbose=False)[0]['jobId']+1
      else:
        jobId=1

      r=SpecificDataRow(tr,jobId,self.url)
      r.parse_and_save()

  def nexthref(self):
    orig=self.getPageRow().xpath('td/a/@href')[0]
    return re.sub(r'jsessionid[^?]+\?','?',orig)

  def pageNums(self):
    currentpagetext=self.getPageRow().xpath('td/text()')[0]
    foo=re.search(r'([0-9]+) of ([0-9]+)',currentpagetext)
    return map(int,[foo.group(1),foo.group(2)])

  def currentPage(self):
    return self.pageNums()[0]

  def lastPage(self):
    return self.pageNums()[1]

  def getTableRows(self):
    "Skip the empty, header and page rows"
    return self.tree.xpath('tr')[2:-1]

  def getHeaderRow(self):
    return self.tree.xpath('tr[position()=2]')[0]
  
  def getPageRow(self):
    return self.tree.xpath('tr[position()=last()]')[0]

  def getcolnames(self):
    return [keyify(td.text_content()) for td in self.getHeaderRow()]

  def rawparse(self):
    colnames=self.getcolnames()
    d=[]
    for tr in self.getTableRows():
      plaintext=[td.text_content() for td in tr.xpath('td')]
      d_row=dict(zip(colnames,plaintext))
      d.append(d_row)
    return d

class ClientTable(JobsTable):
  def parse_and_save(self):
    self._parse_and_save(ClientDataRow,'clients')

class LobbyistTable(JobsTable):
  def parse_and_save(self):
    self._parse_and_save(LobbyistDataRow,'lobbyists')

class DataRow:
  DETAIL_COLNAMES=['detailId','compensation','reimbursement']
  def __init__(self,tr,jobId,url):
    "Takes an lxml tr node"
    self.tr=tr
    self.jobId=jobId
    self.url=url

  def target_and_subject(self):
    nodes=self.tr.xpath('td[position()=last()]/div/text()')
    if 3==len(nodes):
      d={}
      d['target'],d['subject']=nodes[1:3]
    else:
      #http://www.nyc.gov/lobbyistsearch/search?client=10+Gold+L.L.C.&op=&pg_c=2
      d={
        "target":None
      , "subject":None
      }
    return d

  def parse_detail(self):
    nodes=self.tr.xpath('td[position()=last()]/div/table')
    assert 1==len(nodes),nodes
    detail_table=nodes[0]

    d=[]
    for tr in detail_table.xpath('tr[position()>1]'):
      values=[td.text_content() for td in tr.xpath('td')]
      values[0]=keyify(values[0])
      values[1:3]=map(self.money_as_float,values[1:3])
      row=dict(zip(self.DETAIL_COLNAMES,values))
      row['jobId']=self.jobId
      d.append(row)
    return d

  @staticmethod
  def money_as_float(money):
    foo=re.sub(r'[,$]','',money)
    try:
      return float(foo)
    except:
      return None

  def parse_main(self):
    "Depends on a _parse_main function defined for the specific table type"
    d=self._parse_main()
    d.update(self.target_and_subject())
    return d

  @staticmethod
  def parsedate(rawdate):
     return datetime.datetime.strptime(rawdate,'%m/%d/%Y').date()

  def get_td_text_by_position(self,position):
    return self.tr.xpath('td[position()=%d]' % int(position) )[0].text_content().strip()

  def get_td_text_nodes_by_position(self,position):
    return '\n'.join(self.tr.xpath('td[position()=%d]/text()') % int(position)).strip()

  @staticmethod
  def linklist_from_cell(td,textname="text",hrefname="href",sourcename="source",sourcevalue=None):
    "Extract a list of links from one td node"
    a_nodes=td.xpath('a')
    d=[{textname:a.text,hrefname:a.attrib['href']} for a in a_nodes]
    if sourcevalue!=None:
      for row in d:
        row[sourcename]=sourcevalue
    return d


class ClientDataRow(DataRow):
  "More parsing on a client data row"
  def parse_and_save(self):
    job=self.parse_main()
    lobbyists=self.parse_lobbyists()
    detail=self.parse_detail()

    save(['jobId'],job,'clients',verbose=False)
    save([],lobbyists,'clients_lobbyists',verbose=False)
    save([],detail,'clients_details',verbose=False)
    save(['jobId','sourceUrl'],{"jobId":self.jobId,"sourceUrl":self.url},'clients_urls')

  def parse_lobbyists(self):
    td=self.tr.xpath('td[position()=5]')[0]
    return self.linklist_from_cell(
      td
    , textname="lobbyist"
    , hrefname="lobbyist_url"
    , sourcename="jobId"
    , sourcevalue=self.jobId
    )

  def _parse_main(self):
    "Stuff that fits in one table"
    lobbyist_url_nodes=self.tr.xpath('td[position()=6]/a/@href')
    assert len(lobbyist_url_nodes)==1,lobbyist_url_nodes

    return {
      'jobId':self.jobId
    , 'client-name':self.get_td_text_by_position(1)
    , 'client-address':self.get_td_text_by_position(2)
    , 'begin-date':self.parsedate(self.get_td_text_by_position(3))
    , 'end-date':self.parsedate(self.get_td_text_by_position(4))
    , 'lobbyist-address':self.get_td_text_by_position(6)
    , 'lobbyist-url':lobbyist_url_nodes[0]
    , 'lobbyist-officer':self.get_td_text_by_position(7)
    }


class LobbyistDataRow(DataRow):
  "More parsing on a client data row"
  def parse_and_save(self):
    job=self.parse_main()
    lobbyists=self.parse_lobbyists()
    detail=self.parse_detail()

    save(['jobId'],job,'lobbyists',verbose=False)
    save([],lobbyists,'lobbyists_lobbyists',verbose=False)
    save([],detail,'lobbyists_details',verbose=False)
    save(['jobId','sourceUrl'],{"jobId":self.jobId,"sourceUrl":self.url},'lobbyists_urls')

  def parse_lobbyists(self):
    td=self.tr.xpath('td[position()=5]')[0]
    return self.linklist_from_cell(
      td
    , textname="lobbyist"
    , hrefname="lobbyist_url"
    , sourcename="jobId"
    , sourcevalue=self.jobId
    )

  def _parse_main(self):
    "Stuff that fits in one table"
    client_url_nodes=self.tr.xpath('td[position()=4]/a/@href')
    assert len(client_url_nodes)==1,lobbyist_url_nodes

    return {
      'jobId':self.jobId
    , 'lobbyist-principal':self.get_td_text_by_position(1)
    , 'lobbyist-address':self.get_td_text_by_position(2)
    , 'lobbyist-officer':self.get_td_text_by_position(3)
    , 'client-address':self.get_td_text_by_position(4)
    , 'client-url':client_url_nodes[0]
    , 'begin-date':self.parsedate(self.get_td_text_by_position(6))
    , 'end-date':self.parsedate(self.get_td_text_by_position(7))
    }



def legend():
  x=fromstring(get('http://www.nyc.gov/lobbyistsearch/helpguide.html').content)

  d=[]
  column_base={
    "name":""
  , "value":""
  }
  column=copy(column_base)
  for p in x.xpath('id("fielddesc")/../../p'):
    potential_name=''.join(p.xpath('b[span[@class="bodytext_bold_orange"]]/text()'))
    if potential_name=='' and p.text!=None:
      column['value']+=p.text+'\n'
    elif potential_name!='':
      d.append(column)
      column=copy(column_base)
      column['name']=potential_name
  return d[1:]

# --------------------------------------------------
# Go
def clear():
  execute('DROP TABLE IF EXISTS clients')
  execute('DROP TABLE IF EXISTS clientsraw')
  execute('DROP TABLE IF EXISTS clients_urls')
  execute('DROP TABLE IF EXISTS clients_lobbyists')
  execute('DROP TABLE IF EXISTS clients_details')
  execute('DROP TABLE IF EXISTS lobbyists')
  execute('DROP TABLE IF EXISTS lobbyistsraw')
  execute('DROP TABLE IF EXISTS lobbyists_urls')
  execute('DROP TABLE IF EXISTS lobbyists_lobbyists')
  execute('DROP TABLE IF EXISTS lobbyists_details')
  save_var('previous_href',None)

def demo():
  parse_result('search?client=FIFTEEN%20CENTRAL%20PARK%20WEST%20CONDOMINIUM')
  parse_result('search?lobbyist=victoria+contino')

#browsepage('2008','All Lobbyists')
#demo()

#Dunno why I needed to fix this manually...
#save_var('previous_href','search?client=104+Charlton+L+L+C')
#drop_above_jobId(21965,CLIENT_TABLES)

#save([],legend(),'legend')

main2()