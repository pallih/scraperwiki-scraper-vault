"""
Scrape information about contributers and the urls of the contributers' popups.
Save all of these to the data store.
"""

import scraperwiki
from mechanize import Browser
from lxml.html import fromstring

URLS={
  "choose":"http://www.elections.ca/scripts/webpep/fin2/select_election.aspx?entity=1&lang=e"
, "search":"http://www.elections.ca/scripts/webpep/fin2/select_search_option.aspx"
}

def main():
  b=Browser()
  r=b.open(URLS['choose'])
  r=PostForm_by_id(b,r,'rptGeneralElections_ctl00_lnkElection')
#  r=PostForm_by_id(b,r,'rptSearchOptions_ctl00_lnkOptionTitle')
  print r.read()

def PostForm(b,strActionPage, strFieldNames, strFieldValues):
  """Post given the browser at the right page"""
  b.select_form(nr=0) 
  #b["page"].value = 1
  #b["action"] = strActionPage
  #b["id"] = ctlItem
  #b["PrevReturn"] = "0"
  r=b.submit()
  return r

def PostForm_by_id(b,r,id):
  raw=r.read()
  xml=fromstring(raw)
  args=[b]
  args.extend(xml.get_element_by_id(id).attrib['href'].replace('javascript:PostForm(','').replace(');','').replace("'",'').split(','))
  r=apply(PostForm,args)
  return r

main()