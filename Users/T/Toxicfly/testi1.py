import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=testi&query=select+*+from+`swdata`&apikey=")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:
 line = line + 1 
 print row
 html = scraperwiki.scrape(row[0])
 print html
 scrape_data = scrape("""
{*
<span itemprop="name">{{ [mobile].[title] }}</span>

            <h2 class="acc_d"><span></span>Processor Description</h2>
            <div class="acc_dTD clearfix">
                <table width="100%" class="tabfs">
                    
                        <tr><td width="30%"><span><a href="/glossary/processor/673/30">Processor</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[processor] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/speed/9482/30">Speed</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[processorspeed] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/cache/9492/30">Cache</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[processorcache] }}</td></tr>
                    
                </table>
            </div>

<tr><td width="30%"><span><a href="/glossary/capacity/11392/30">Capacity</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[ram] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/type/9532/30">Type</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[ramtype] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/speed/9542/30">Speed</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[ramspeed] }}</td></tr>
                    
        <td width="70%">{{ [mobile].[hdd] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/speed-rpm/7272/30">Speed (RPM)</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[hddspeed] }}</td></tr>
*}
""", html=html);

 data = [{'title':p['title'][0], 'processor':p['processor'][0], 'Processor Speed':p['processorspeed'][0], 'Processor Cache':p['processorcache'][0], 'RAM':p['ram'][0], 'Ram Type':p['ramtype'][0], 'Ram Speed':p['ramspeed'][0], 'Hard Disk Capacity':p['hdd'][0], 'Hard Disk Speed':p['hddspeed'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["title"], data=data)







