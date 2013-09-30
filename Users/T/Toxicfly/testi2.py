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


                    
                        <tr><td width="30%"><span><a href="/glossary/ethernet-port-nos/9602/30">Ethernet Port (Nos)</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[ethernetport] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/ethernet-type/9612/30">Ethernet Type</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[ethernettype] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/wifi-type/9622/30">WiFi Type</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[wifitype] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/wifi-speed/9632/30">Wifi Speed</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[wifispeed] }}</td></tr>
                    

                    
                        <tr><td width="30%"><span><a href="/glossary/audio-solution/7612/30">Audio Solution</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiosolution] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/channels/7622/30">Channels</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiochannels] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/speakers/9642/30">Speakers</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiospeakers] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/sound-technologies/9652/30">Sound Technologies</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiosoundtech] }}</td></tr>



   
                    
       


     
*}
""", html=html);

 data = [{'name':p['title'][0], 'Audio':p['audiosolution'][0], 'Channels':p['audiochannels'][0], 'Speakers':p['audiospeakers'][0], 'Sound Technology':p['audiosoundtech'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["name"], data=data)



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


                    
                        <tr><td width="30%"><span><a href="/glossary/ethernet-port-nos/9602/30">Ethernet Port (Nos)</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[ethernetport] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/ethernet-type/9612/30">Ethernet Type</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[ethernettype] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/wifi-type/9622/30">WiFi Type</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[wifitype] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/wifi-speed/9632/30">Wifi Speed</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[wifispeed] }}</td></tr>
                    

                    
                        <tr><td width="30%"><span><a href="/glossary/audio-solution/7612/30">Audio Solution</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiosolution] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/channels/7622/30">Channels</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiochannels] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/speakers/9642/30">Speakers</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiospeakers] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/sound-technologies/9652/30">Sound Technologies</a>&nbsp;
                        
                        </span></td>
                        <td width="70%">{{ [mobile].[audiosoundtech] }}</td></tr>



   
                    
       


     
*}
""", html=html);

 data = [{'name':p['title'][0], 'Audio':p['audiosolution'][0], 'Channels':p['audiochannels'][0], 'Speakers':p['audiospeakers'][0], 'Sound Technology':p['audiosoundtech'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["name"], data=data)



