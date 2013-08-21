import scraperwiki
from  lxml.html import document_fromstring , parse , submit_form
# Blank Python

page = parse('http://www.discoverireland.ie/CMSPages/PortalTemplate.aspx?aliaspath=%2fSearch%2fResults&lcid=1&catid=10041&countyid=23&reftype=1').getroot()
data=[a.attrib['href'] for a in page.xpath("//table[@id='p_lt_zoneMain_pphMain_pphMain_lt_zoneSearchResultsPanel_DI_SearchResultsPanel_1_gvResults']/tr/td/div[@class='article-results border-base']/div[@class='article-results-details']/a[@class='arrow-link fc-color mar-t-10']")]
imgs=[a.attrib['style'] for a in page.xpath("//table[@id='p_lt_zoneMain_pphMain_pphMain_lt_zoneSearchResultsPanel_DI_SearchResultsPanel_1_gvResults']/tr/td/div[@class='article-results border-base']/div[@class='img-box']/a")]
print imgs
for i in range(len(data)):
   recpage = parse('http://www.discoverireland.ie'+data[i]).getroot()
   name=[a.text for a in recpage.xpath("//form/div[@id='wrap-main']/div[@class='column-tourist-main tc']/div[@class='column-tourist-wide']/h2[@id='TcsEntityName']")]
   print name
   description=[a.text for a in recpage.xpath("//form/div[@id='wrap-main']/div[@class='column-tourist-main tc']/div[@class='column-tourist-wide']/div[@class='eq']/div/p")]
   print description
   lat=[a.value for a in recpage.xpath("//input[@name='p$lt$zoneMain$pphMain$pphMain$lt$ucWalkingHikingTouristItem$ucThingsToDoNearby$txtLatitude']")]
   print lat
   longg=[a.value for a in recpage.xpath("//input[@name='p$lt$zoneMain$pphMain$pphMain$lt$ucWalkingHikingTouristItem$ucThingsToDoNearby$txtLongitude']")]
   print longg
   address=[a for a in recpage.xpath("//form/div[@id='wrap-main']/div[@class='column-tourist-main tc']/div[@class='column-tourist-wide']/div[@class='eq']/div[@class='column-tourist-two']/div[@class='fc-color']/p//text()")]
   print address;
   
   
   record={"url":data[i],"name":name,"description":description,"lat":lat,"long" :longg , "address":address ,"img":imgs[i]}

   scraperwiki.datastore.save(["url","name","description","lat","long","address","img"],record,table_name="Asset")









