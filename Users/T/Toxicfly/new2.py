import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=new_3&query=select+*+from+`swdata`&apikey=")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:
 line = line + 1 
 print row
 html = scraperwiki.scrape("http://www.homeseekers.com/"+row[0])
 print html
 scrape_data = scrape("""
{*
<span id="Master_lblAgentName" class="formheader ai_agent_name">{{ [mobile].[title] }}</span>

 <span id="Master_lblAgentPhoneNumbers"><div class="ai_phone_main office">{{ [mobile].[main] }}</div><div class="ai_phone_direct office"></div><div class="ai_phone_personal fax"></div><div class="ai_phone_mobile">{{ [mobile].[mob] }}</div></span>
    
*}
""", html=html);

 data = [{'name':p['title'][0], 'Main':p['main'][0], 'Mobile1':p['mob'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=[], data=data)
