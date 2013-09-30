from  lxml.html import document_fromstring , parse , submit_form
import scraperwiki
import re
from datetime import datetime
import time
import random
import mechanize, urllib, urllib2
import lxml.html
from BeautifulSoup import BeautifulSoup
import os

def saveInDataStore(names,urls):
  for i in range(len(urls)):
   data={"name":names[i] , "url":urls[i]}
   scraperwiki.datastore.save(["name", "url"],data)
  



def getAndSaveAssetURL(button_value ,first_index):
  page = parse('http://www.semic.eu/semic/view/snav/assetRepository.xhtml').getroot()
  if first_index!=0 :
   page.forms[2].fields["j_id81:j_id119:0:j_id340"] = str(first_index)
   page.forms[2].fields["j_id81:j_id119:0:j_id481"] = button_value
   page.forms[2].fields["j_id81"] ="j_id81"
   page.forms[2].fields["navpage"] = "aece014c-5019-4751-a728-5090322ab3f9" 
   page.forms[2].fields["j_id81:j_id103"] = ["ASSET"]
   page.forms[2].fields["j_id81:j_id119:0:j_id341"] = "sortBy_name_asc"
   result = parse(submit_form(page.forms[2],extra_values={'j_id81:j_id119:0:j_id481': button_value})).getroot()
   names=[a.text for a in result.xpath("//td[@class='textColumn']/a")]
   urls=[a.attrib['href'] for a in result.xpath("//td[@class='textColumn']/a")]
   saveInDataStore(names,urls)
   print len(urls)
  else :
   result = parse(submit_form(page.forms[2])).getroot()
   names=[a.text for a in result.xpath("//td[@class='textColumn']/a")]
   urls=[a.attrib['href'] for a in result.xpath("//td[@class='textColumn']/a")]
   saveInDataStore(names,urls)


def fillDataStore():
  count = 0
  while (count <= 36):
     print 'The count is:', count
     if count !=0:
      first_index=count*15
      button_index_one=first_index+1
      button_index_two=first_index+15
      button_value=str(button_index_one)+" - "+str(button_index_two)
      print button_value ,  first_index
      getAndSaveAssetURL(button_value ,first_index)
     else :
      first_index=0
      button_index_one=count+1
      button_index_two=count+15
      button_value=str(button_index_one)+" - "+str(button_index_two)
      print 'ff'
      getAndSaveAssetURL(button_value ,first_index)
     count = count + 1


def getURLs():
  dictionary=scraperwiki.sqlite.execute("select url from swdata")
  data=dictionary['data']
  return data




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
  rel_col1=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]")]
  rel_name1=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[1]/a")]
  #---
  rel_col2=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]")]
  rel_name2= [a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[2]/a")]
  #---
  rel_col3=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]")]
  rel_name3=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[3]/a")]
  #---
  rel_col4=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]")]
  rel_name4=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[4]/a")]
  #---
  rel_col5=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]")]
  rel_name5=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[5]/a")]
  #---
  rel_col6=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]")]
  rel_name6=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[6]/a")]
  
  #status
  states= [a.attrib['alt'] for a in result.xpath("//div[@class='states']/img[@alt!='This state is in the past']")]
  #Related Projects
  rel_projects= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[5]/div/a")]
  #Provided by
  
  #Asset Agent 
  agent= [a.attrib['href'] for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div/div/a")]
  #description 
  descr=[a.text for a in result.xpath("//div[@class='noedit']/p[2]")]
  #Asset Owner
  owner=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div[2]")]
  print owner
  data={"name":title[0].replace('\\n', '').replace('\\t', '') , "url":url,"asset_id":asset_id[0].replace('\\n', '').replace('\\t', ''),"pub_date":pub_date[0].replace('\\t', '').replace('\\n', ''),"last_change":last_change[0].replace('\\t', '').replace('\\n', ''),"country":country,"tags":tags,"domain":domain,"descr":descr,"rel_projects":rel_projects,"agent":agent,"owner":owner,"state":states[0],"rel_col1":rel_col1,"rel_col2":rel_col2,"rel_col3":rel_col3,"rel_col4":rel_col4,"rel_col5":rel_col5,"rel_col6":rel_col6,"rel_name1":rel_name1,"rel_name2":rel_name2,"rel_name3":rel_name3,"rel_name4":rel_name4,"rel_name5":rel_name5,"rel_name6":rel_name6}
  scraperwiki.datastore.save(["url"],data,table_name="Asset")



def releasesData(url):
  page = parse(url).getroot()
  result2 = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  result3 = [a.attrib['href'] for a in result2.xpath("//a[@id='j_id82:j_id636']")]
  if not result3 :
   print 'empty'
  else :
   print result3[0]
   result =parse('http://www.semic.eu'+result3[0]).getroot()
   data=[a.attrib['href'] for a in result.xpath("//table[@class='releases']/tbody/tr/td[1]/a")]
   print data
   for link in data:
     release_page = parse('http://www.semic.eu/semic/view/Asset/'+link).getroot()
     #Publication date and state
     pub_date_state= [a.text for a in release_page.xpath("//div[@class='releaseDownloads']/div/div[@class='alignLeft widthAuto']")]
     if not pub_date_state:
      pub_date_state=[]
     #release No
     no= [a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[1]")]
     if not no:
      no=[]  
     #Documentation language(s)
     lang=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
     if not lang:
      lang=[]  
     #Release Contents
     release=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[4]")] 
     #Lisence Class
     lisence_class=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[5]")]
     if not lisence_class:
      lisence_class=[]
     #Lisence
     lisence=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[6]")]
     if not lisence:
      lisence=[]
     #Notes
     notes=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[9]")]
     if not notes:
      notes=[]
     data={"link":link}
     data["pub_date_state"]=pub_date_state[0].replace('\n\t\t\t\t\t\t\t', '')
     data["url"]=url
     data["number"]=no[0].replace('\n\t\t\t\t\t\t\t', '')
     data["lang"]=lang
     data["lisence_class"]=lisence_class[0].replace('\n\t\t\t\t\t\t\t', '')
     data["lisence"]=lisence[0].replace('\n\t\t\t\t\t\t\t', '')
     data["notes"]=notes[0].replace('\n\t\t\t\t\t\t\t', '')
     print release
     if not release:
      release=[] 
     else:
      for kinds in release:
       kindarr=kinds.split(',')
       for kind in kindarr:
         print kind
         if kind.find('Other')!=-1:
          data["content"]=kind
         if kind.find('UML')!=-1 or kind.find('UMM')!=-1 or  kind .find( 'BPMN') !=-1 or  kind .find( 'FMC') !=-1:
          data["Model"]=kind
         if kind .find( 'XML Schema') !=-1 or kind.find('Relax NG') !=-1 or  kind .find( 'Schematron') !=-1 or  kind .find( 'WSDL')!=-1 or  kind .find('ebXML Process Def')!=-1:
          data["Syntax"]=kind
         if kind .find( 'Codelists') !=-1 or kind .find( 'Mappings') !=-1 or  kind .find( 'Taxonomy') !=-1 or  kind .find( 'Ontology') !=-1:  
          data["Semantic"]=kind
         if kind .find( 'Core Components') !=-1:
          data["Abstract"]=kind
     print 'url :'+url
     if not data:
      print 'data is empty'
     else:
      print data
      scraperwiki.datastore.save(["link"],data,table_name="Release")


def runAll():
  #fillDataStore()
  data=getURLs()
  print  data[0][0]
  for url in data:
   assetData('http://www.semic.eu'+str(url[0]))
   #releasesData('http://www.semic.eu'+str(url[0]))


def getReleaseCol():
 dictionary=scraperwiki.sqlite.execute("select * from Release")
 
 for row in dictionary['data']:
   record={"link":row[9],"pub_date_state":row[0], "url":row[5],"number":row[8],"lang":row[1],"lisence_class":row[6],"lisence":row[3],"notes":row[7]}
   data=row[2].replace('[','').replace(']','').replace('\'','').replace('\\n\\t\\t\\t\\t\\t\\t\\t','')
   data=data.split(',')
   for kind in data:
    if kind == 'Other':
       record["content_type"]=kind
    if kind == 'UML' or kind == 'UMM' or  kind == 'BPMN' or  kind == 'FMC':
       record["Model"]=kind
    if kind == 'XML Schema' or kind == 'Relax NG' or  kind == 'Schematron' or  kind == 'WSDL' or  kind == 'ebXML Process Def':  
       record["Syntax"]=kind
    if kind == 'Codelists' or kind == 'Mappings' or  kind == 'Taxonomy' or  kind == 'Ontology':  
       record["Semantic"]=kind
    if kind == 'Core Components':
       record["Abstract"]=kind
    

   scraperwiki.datastore.save(["link"],record,table_name="Release_with_coulmn")

#getReleaseCol()
runAll()
#scraperwiki.sqlite.execute("drop table Asset")
#scraperwiki.sqlite.execute("drop table Release")

#releasesData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=19')from  lxml.html import document_fromstring , parse , submit_form
import scraperwiki
import re
from datetime import datetime
import time
import random
import mechanize, urllib, urllib2
import lxml.html
from BeautifulSoup import BeautifulSoup
import os

def saveInDataStore(names,urls):
  for i in range(len(urls)):
   data={"name":names[i] , "url":urls[i]}
   scraperwiki.datastore.save(["name", "url"],data)
  



def getAndSaveAssetURL(button_value ,first_index):
  page = parse('http://www.semic.eu/semic/view/snav/assetRepository.xhtml').getroot()
  if first_index!=0 :
   page.forms[2].fields["j_id81:j_id119:0:j_id340"] = str(first_index)
   page.forms[2].fields["j_id81:j_id119:0:j_id481"] = button_value
   page.forms[2].fields["j_id81"] ="j_id81"
   page.forms[2].fields["navpage"] = "aece014c-5019-4751-a728-5090322ab3f9" 
   page.forms[2].fields["j_id81:j_id103"] = ["ASSET"]
   page.forms[2].fields["j_id81:j_id119:0:j_id341"] = "sortBy_name_asc"
   result = parse(submit_form(page.forms[2],extra_values={'j_id81:j_id119:0:j_id481': button_value})).getroot()
   names=[a.text for a in result.xpath("//td[@class='textColumn']/a")]
   urls=[a.attrib['href'] for a in result.xpath("//td[@class='textColumn']/a")]
   saveInDataStore(names,urls)
   print len(urls)
  else :
   result = parse(submit_form(page.forms[2])).getroot()
   names=[a.text for a in result.xpath("//td[@class='textColumn']/a")]
   urls=[a.attrib['href'] for a in result.xpath("//td[@class='textColumn']/a")]
   saveInDataStore(names,urls)


def fillDataStore():
  count = 0
  while (count <= 36):
     print 'The count is:', count
     if count !=0:
      first_index=count*15
      button_index_one=first_index+1
      button_index_two=first_index+15
      button_value=str(button_index_one)+" - "+str(button_index_two)
      print button_value ,  first_index
      getAndSaveAssetURL(button_value ,first_index)
     else :
      first_index=0
      button_index_one=count+1
      button_index_two=count+15
      button_value=str(button_index_one)+" - "+str(button_index_two)
      print 'ff'
      getAndSaveAssetURL(button_value ,first_index)
     count = count + 1


def getURLs():
  dictionary=scraperwiki.sqlite.execute("select url from swdata")
  data=dictionary['data']
  return data




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
  rel_col1=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[1]")]
  rel_name1=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[1]/a")]
  #---
  rel_col2=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[2]")]
  rel_name2= [a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[2]/a")]
  #---
  rel_col3=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[3]")]
  rel_name3=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[3]/a")]
  #---
  rel_col4=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[4]")]
  rel_name4=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[4]/a")]
  #---
  rel_col5=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[5]")]
  rel_name5=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[5]/a")]
  #---
  rel_col6=[a.text for a in result.xpath("//dd[@class='relatedAssets']/div[6]")]
  rel_name6=[a.attrib['href'] for a in result.xpath("//dd[@class='relatedAssets']/div[6]/a")]
  
  #status
  states= [a.attrib['alt'] for a in result.xpath("//div[@class='states']/img[@alt!='This state is in the past']")]
  #Related Projects
  rel_projects= [a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[5]/div/a")]
  #Provided by
  
  #Asset Agent 
  agent= [a.attrib['href'] for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div/div/a")]
  #description 
  descr=[a.text for a in result.xpath("//div[@class='noedit']/p[2]")]
  #Asset Owner
  owner=[a.text for a in result.xpath("//dl[@class='assetDefinition clearfix']/dd[6]/div[2]")]
  print owner
  data={"name":title[0].replace('\\n', '').replace('\\t', '') , "url":url,"asset_id":asset_id[0].replace('\\n', '').replace('\\t', ''),"pub_date":pub_date[0].replace('\\t', '').replace('\\n', ''),"last_change":last_change[0].replace('\\t', '').replace('\\n', ''),"country":country,"tags":tags,"domain":domain,"descr":descr,"rel_projects":rel_projects,"agent":agent,"owner":owner,"state":states[0],"rel_col1":rel_col1,"rel_col2":rel_col2,"rel_col3":rel_col3,"rel_col4":rel_col4,"rel_col5":rel_col5,"rel_col6":rel_col6,"rel_name1":rel_name1,"rel_name2":rel_name2,"rel_name3":rel_name3,"rel_name4":rel_name4,"rel_name5":rel_name5,"rel_name6":rel_name6}
  scraperwiki.datastore.save(["url"],data,table_name="Asset")



def releasesData(url):
  page = parse(url).getroot()
  result2 = parse(submit_form(page.forms[2],extra_values={'j_id82:j_id510': 'Release downloads'})).getroot()
  result3 = [a.attrib['href'] for a in result2.xpath("//a[@id='j_id82:j_id636']")]
  if not result3 :
   print 'empty'
  else :
   print result3[0]
   result =parse('http://www.semic.eu'+result3[0]).getroot()
   data=[a.attrib['href'] for a in result.xpath("//table[@class='releases']/tbody/tr/td[1]/a")]
   print data
   for link in data:
     release_page = parse('http://www.semic.eu/semic/view/Asset/'+link).getroot()
     #Publication date and state
     pub_date_state= [a.text for a in release_page.xpath("//div[@class='releaseDownloads']/div/div[@class='alignLeft widthAuto']")]
     if not pub_date_state:
      pub_date_state=[]
     #release No
     no= [a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[1]")]
     if not no:
      no=[]  
     #Documentation language(s)
     lang=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[3]/a/span")]
     if not lang:
      lang=[]  
     #Release Contents
     release=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[4]")] 
     #Lisence Class
     lisence_class=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[5]")]
     if not lisence_class:
      lisence_class=[]
     #Lisence
     lisence=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[6]")]
     if not lisence:
      lisence=[]
     #Notes
     notes=[a.text for a in release_page.xpath("//dl[@class='assetDefinition clearfix']/dd[9]")]
     if not notes:
      notes=[]
     data={"link":link}
     data["pub_date_state"]=pub_date_state[0].replace('\n\t\t\t\t\t\t\t', '')
     data["url"]=url
     data["number"]=no[0].replace('\n\t\t\t\t\t\t\t', '')
     data["lang"]=lang
     data["lisence_class"]=lisence_class[0].replace('\n\t\t\t\t\t\t\t', '')
     data["lisence"]=lisence[0].replace('\n\t\t\t\t\t\t\t', '')
     data["notes"]=notes[0].replace('\n\t\t\t\t\t\t\t', '')
     print release
     if not release:
      release=[] 
     else:
      for kinds in release:
       kindarr=kinds.split(',')
       for kind in kindarr:
         print kind
         if kind.find('Other')!=-1:
          data["content"]=kind
         if kind.find('UML')!=-1 or kind.find('UMM')!=-1 or  kind .find( 'BPMN') !=-1 or  kind .find( 'FMC') !=-1:
          data["Model"]=kind
         if kind .find( 'XML Schema') !=-1 or kind.find('Relax NG') !=-1 or  kind .find( 'Schematron') !=-1 or  kind .find( 'WSDL')!=-1 or  kind .find('ebXML Process Def')!=-1:
          data["Syntax"]=kind
         if kind .find( 'Codelists') !=-1 or kind .find( 'Mappings') !=-1 or  kind .find( 'Taxonomy') !=-1 or  kind .find( 'Ontology') !=-1:  
          data["Semantic"]=kind
         if kind .find( 'Core Components') !=-1:
          data["Abstract"]=kind
     print 'url :'+url
     if not data:
      print 'data is empty'
     else:
      print data
      scraperwiki.datastore.save(["link"],data,table_name="Release")


def runAll():
  #fillDataStore()
  data=getURLs()
  print  data[0][0]
  for url in data:
   assetData('http://www.semic.eu'+str(url[0]))
   #releasesData('http://www.semic.eu'+str(url[0]))


def getReleaseCol():
 dictionary=scraperwiki.sqlite.execute("select * from Release")
 
 for row in dictionary['data']:
   record={"link":row[9],"pub_date_state":row[0], "url":row[5],"number":row[8],"lang":row[1],"lisence_class":row[6],"lisence":row[3],"notes":row[7]}
   data=row[2].replace('[','').replace(']','').replace('\'','').replace('\\n\\t\\t\\t\\t\\t\\t\\t','')
   data=data.split(',')
   for kind in data:
    if kind == 'Other':
       record["content_type"]=kind
    if kind == 'UML' or kind == 'UMM' or  kind == 'BPMN' or  kind == 'FMC':
       record["Model"]=kind
    if kind == 'XML Schema' or kind == 'Relax NG' or  kind == 'Schematron' or  kind == 'WSDL' or  kind == 'ebXML Process Def':  
       record["Syntax"]=kind
    if kind == 'Codelists' or kind == 'Mappings' or  kind == 'Taxonomy' or  kind == 'Ontology':  
       record["Semantic"]=kind
    if kind == 'Core Components':
       record["Abstract"]=kind
    

   scraperwiki.datastore.save(["link"],record,table_name="Release_with_coulmn")

#getReleaseCol()
runAll()
#scraperwiki.sqlite.execute("drop table Asset")
#scraperwiki.sqlite.execute("drop table Release")

#releasesData('http://www.semic.eu/semic/view/Asset/Asset.SingleView.xhtml?id=19')