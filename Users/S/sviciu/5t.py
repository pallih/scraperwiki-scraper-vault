import scraperwiki    
import lxml.html        
import string
import cgi
import os

html = scraperwiki.scrape("http://www.5t.torino.it/pda/it/arrivi.jsp?n=253") 


root = lxml.html.fromstring(html) 



for li in root.cssselect("li"):     
    cnt = 0;
    for sp in li.cssselect("span[class~='n']"):
        line_str = ''.join(filter(lambda x:x in string.printable, (li.cssselect("h3"))[0].text_content())).replace('Linea','') 
        time_str = ''.join(filter(lambda x:x in string.printable, sp.text_content())).replace('\t','').replace('\n','').replace(' ','')
        data = {
            'line_no': line_str,
            'bus_stop': '253',
            'arrival_time': time_str,
            'pass': str(cnt)
        }
        cnt += 1;
        
        scraperwiki.sqlite.save(unique_keys=['line_no','bus_stop','pass'], data=data)
        d = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
        print d['name']



