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

                                     
                        <tr><td width="30%"><span><a href="/glossary/battery-life/967/30">Battery Life</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[blife] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/battery-cell/9692/30">Battery Cell</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[btype] }}</td></tr>

               

                        <tr><td width="30%"><span><a href="/glossary/os/885/30">OS</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[os] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/version/9752/30">Version</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[osv] }}</td></tr>

               

                        <tr><td width="30%"><span><a href="/glossary/dimensions-w-x-d-x-h/7262/30">Dimensions (W x D x H)</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[dim] }}</td></tr>


                        <tr><td width="30%"><span><a href="/glossary/other-features/9762/30">Other Features</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[misc] }}</td></tr>

              

                        <tr><td width="30%"><span><a href="/glossary/warranty-period/74/30">Warranty Period</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[war] }}</td></tr>

               
*}
""", html=html);

 data = [{'title':p['title'][0], 'Battery Life':p['blife'][0], 'Battery Type':p['btype'][0],'OS':p['os'][0], 'Version':p['osv'][0], 'Dimensions':p['dim'][0], 'Extras':p['misc'][0], 'Warranty':p['war'][0]  } for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["title"], data=data)






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

                                     
                        <tr><td width="30%"><span><a href="/glossary/battery-life/967/30">Battery Life</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[blife] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/battery-cell/9692/30">Battery Cell</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[btype] }}</td></tr>

               

                        <tr><td width="30%"><span><a href="/glossary/os/885/30">OS</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[os] }}</td></tr>
                        <tr><td width="30%"><span><a href="/glossary/version/9752/30">Version</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[osv] }}</td></tr>

               

                        <tr><td width="30%"><span><a href="/glossary/dimensions-w-x-d-x-h/7262/30">Dimensions (W x D x H)</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[dim] }}</td></tr>


                        <tr><td width="30%"><span><a href="/glossary/other-features/9762/30">Other Features</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[misc] }}</td></tr>

              

                        <tr><td width="30%"><span><a href="/glossary/warranty-period/74/30">Warranty Period</a>&nbsp;

                        </span></td>
                        <td width="70%">{{ [mobile].[war] }}</td></tr>

               
*}
""", html=html);

 data = [{'title':p['title'][0], 'Battery Life':p['blife'][0], 'Battery Type':p['btype'][0],'OS':p['os'][0], 'Version':p['osv'][0], 'Dimensions':p['dim'][0], 'Extras':p['misc'][0], 'Warranty':p['war'][0]  } for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["title"], data=data)






