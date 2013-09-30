from  lxml.html import document_fromstring , parse , submit_form
import scraperwiki
import re
from datetime import datetime
import time
import random
import mechanize, urllib, urllib2
import lxml.html
from BeautifulSoup import BeautifulSoup



def assetData(url):
  page = parse(url).getroot()
  result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id131': 'Asset'})).getroot()
  #result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  print [a.text for a in result.xpath("//a")]
  #asset title 
  title= [a.attrib['title'] for a in result.xpath("//div[@class='aboveTabContent clearfix']/h1")]
  #Asset ID:
  asset_id= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[1]")]
  #Initial publication
  pub_date= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[2]/a")]
  #Last change
  last_change= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[3]")]
  #spec
  spec=[a.text for a in result.xpath("//div[@class='noedit']/p[@class='specTabText']")]
  #Represented countries
  country=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[1]/a/span")]
  #Keywords
  tags= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[2]/a/span")]
  #Domains
  domain= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
  #Related Assets
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]/a")]
  
  #Related Projects
  rel_projects= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[5]/div/a")]
  #Provided by
  
  #Asset Agent 
  agent= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div/div/a")]
  #Asset Owner
  owner=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div[2]")]
  data={"name":title[0].replace('\\n', '').replace('\\t', '') , "url":url,"asset_id":asset_id[0].replace('\\n', '').replace('\\t', ''),"pub_date":pub_date[0].replace('\\t', '').replace('\\n', ''),"last_change":last_change[0].replace('\\t', '').replace('\\n', ''),"country":country,"tags":tags,"domain":domain,"rel_projects":rel_projects,"agent":agent,"owner":owner}
  scraperwiki.datastore.save(["name","url","asset_id","pub_date","last_change","country","tags","domain","rel_projects","agent","owner"],data,table_name="Asset")

def releasesData(url):
  page = parse(url).getroot()
  result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  data=[a.attrib['href'] for a in result.xpath("//table[@class='releases']/tbody/tr/td[1]/a")]
  print data
  for link in data:
   release_page = parse('http://www.semic.eu/semic/view/Asset/'+link).getroot()
   #Publication date and state
   pub_date_state= [a.text for a in release_page.xpath("//div[@class='releaseDownloads']/div/div[@class='alignLeft widthAuto']")]
   #release No
   no= [a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[1]")]
   print no[0].replace('\\t', '')
   print no[0].replace('\\n', '')  
   #Documentation language(s)
   lang=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
   #Release Contents
   release=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[4]")]
   #Lisence Class
   lisence_class=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[5]")]
   #Lisence
   lisence=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[6]")]
   #Notes
   notes=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[9]")]
   data={"pub_date_state":pub_date_state[0].replace('\\n', '').replace('\\t', '') , "url":url,"number":no[0].replace('\\n', '').replace('\\t', ''),"lang":lang,"release":release, "lisence_class":lisence_class[0].replace('\\n', '').replace('\\t', ''),"lisence":lisence[0].replace('\\n', '').replace('\\t', ''),"notes":notes[0].replace('\\n', '').replace('\\t', '')}
  scraperwiki.datastore.save(["pub_date_state","url","number","lang","release","lisence_class","lisence","notes"],data,table_name="release")









#assetData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=270')
releasesData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=270')
#scraperwiki.sqlite.execute("drop table Asset")
from  lxml.html import document_fromstring , parse , submit_form
import scraperwiki
import re
from datetime import datetime
import time
import random
import mechanize, urllib, urllib2
import lxml.html
from BeautifulSoup import BeautifulSoup



def assetData(url):
  page = parse(url).getroot()
  result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id131': 'Asset'})).getroot()
  #result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  print [a.text for a in result.xpath("//a")]
  #asset title 
  title= [a.attrib['title'] for a in result.xpath("//div[@class='aboveTabContent clearfix']/h1")]
  #Asset ID:
  asset_id= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[1]")]
  #Initial publication
  pub_date= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[2]/a")]
  #Last change
  last_change= [a.text for a in result.xpath("//div[@class='alignLeft editAssetButton']/span[3]")]
  #spec
  spec=[a.text for a in result.xpath("//div[@class='noedit']/p[@class='specTabText']")]
  #Represented countries
  country=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[1]/a/span")]
  #Keywords
  tags= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[2]/a/span")]
  #Domains
  domain= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
  #Related Assets
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]/a")]
  #---
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]")]
  print [a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]/a")]
  
  #Related Projects
  rel_projects= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[5]/div/a")]
  #Provided by
  
  #Asset Agent 
  agent= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div/div/a")]
  #Asset Owner
  owner=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div[2]")]
  data={"name":title[0].replace('\\n', '').replace('\\t', '') , "url":url,"asset_id":asset_id[0].replace('\\n', '').replace('\\t', ''),"pub_date":pub_date[0].replace('\\t', '').replace('\\n', ''),"last_change":last_change[0].replace('\\t', '').replace('\\n', ''),"country":country,"tags":tags,"domain":domain,"rel_projects":rel_projects,"agent":agent,"owner":owner}
  scraperwiki.datastore.save(["name","url","asset_id","pub_date","last_change","country","tags","domain","rel_projects","agent","owner"],data,table_name="Asset")

def releasesData(url):
  page = parse(url).getroot()
  result = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  data=[a.attrib['href'] for a in result.xpath("//table[@class='releases']/tbody/tr/td[1]/a")]
  print data
  for link in data:
   release_page = parse('http://www.semic.eu/semic/view/Asset/'+link).getroot()
   #Publication date and state
   pub_date_state= [a.text for a in release_page.xpath("//div[@class='releaseDownloads']/div/div[@class='alignLeft widthAuto']")]
   #release No
   no= [a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[1]")]
   print no[0].replace('\\t', '')
   print no[0].replace('\\n', '')  
   #Documentation language(s)
   lang=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
   #Release Contents
   release=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[4]")]
   #Lisence Class
   lisence_class=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[5]")]
   #Lisence
   lisence=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[6]")]
   #Notes
   notes=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[9]")]
   data={"pub_date_state":pub_date_state[0].replace('\\n', '').replace('\\t', '') , "url":url,"number":no[0].replace('\\n', '').replace('\\t', ''),"lang":lang,"release":release, "lisence_class":lisence_class[0].replace('\\n', '').replace('\\t', ''),"lisence":lisence[0].replace('\\n', '').replace('\\t', ''),"notes":notes[0].replace('\\n', '').replace('\\t', '')}
  scraperwiki.datastore.save(["pub_date_state","url","number","lang","release","lisence_class","lisence","notes"],data,table_name="release")









#assetData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=270')
releasesData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=270')
#scraperwiki.sqlite.execute("drop table Asset")
