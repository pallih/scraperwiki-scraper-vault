import scraperwiki
from scrapemark import scrape
import scraperwiki

for page in range(1,40):
  URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=9" #Managed
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOFEA3" #Customer Service
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOGEA3" #Marketing
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOHEA3" #IT & Admin
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOIEA3" #HR
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOJEA3" #Finance
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOKEA3" #ERP
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOLEA3" #Collabration
  #URL = "https://appexchange.salesforce.com/category/analytics" #Analytics
  
  
  print URL
  html = scraperwiki.scrape(URL)
  scrape_data = scrape("""
   {*
   
   <a class="tile-title" href="{{ [mobile].[link] }}" id="{{ [mobile].[id] }}" title="{{ [mobile].[title1] }}"></a>
   
   *}
   """, html=html);

  data = [{'Title':p['title1'][0], 'URL':p['link'][0], 'ID':p['id'][0], 'Format':'Managed'} for p in scrape_data['mobile']]

  scraperwiki.sqlite.save(unique_keys=["URL"], data=data)
import scraperwiki
from scrapemark import scrape
import scraperwiki

for page in range(1,40):
  URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=9" #Managed
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOFEA3" #Customer Service
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOGEA3" #Marketing
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOHEA3" #IT & Admin
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOIEA3" #HR
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOJEA3" #Finance
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOKEA3" #ERP
  #URL = "https://appexchange.salesforce.com/results?pageNo="+str(page)+"&filter=a0L3000000OvSOLEA3" #Collabration
  #URL = "https://appexchange.salesforce.com/category/analytics" #Analytics
  
  
  print URL
  html = scraperwiki.scrape(URL)
  scrape_data = scrape("""
   {*
   
   <a class="tile-title" href="{{ [mobile].[link] }}" id="{{ [mobile].[id] }}" title="{{ [mobile].[title1] }}"></a>
   
   *}
   """, html=html);

  data = [{'Title':p['title1'][0], 'URL':p['link'][0], 'ID':p['id'][0], 'Format':'Managed'} for p in scrape_data['mobile']]

  scraperwiki.sqlite.save(unique_keys=["URL"], data=data)
