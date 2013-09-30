import scraperwiki
import lxml.html
import re
import dateutil
from datetime import *

html =  scraperwiki.scrape("http://bicincitta.tobike.it/frmLeStazioni.aspx?ID=80");

root = lxml.html.fromstring(html)

#pay attention, time in UTC
now = datetime.now();

print now

for el in root.cssselect("li.rrItem"):
    div_id_name = el[0].attrib["id"]
    station_name_element = el.cssselect("span.Stazione")[0];
    station_name = station_name_element.text_content();
    station_red_element = el.cssselect("span.Red")[0];
    info_string = station_red_element.text_content();
    int_list = re.findall(r'\d+',info_string)    
    #print int_list
    data = {      
        'stazione': station_name,      
        'bici_libere' : int(int_list[0]),     
        'posti_disponibili' : int(int_list[1]),
        'data_ora' : now
    }
    scraperwiki.sqlite.save(unique_keys=['stazione','data_ora'], data=data)import scraperwiki
import lxml.html
import re
import dateutil
from datetime import *

html =  scraperwiki.scrape("http://bicincitta.tobike.it/frmLeStazioni.aspx?ID=80");

root = lxml.html.fromstring(html)

#pay attention, time in UTC
now = datetime.now();

print now

for el in root.cssselect("li.rrItem"):
    div_id_name = el[0].attrib["id"]
    station_name_element = el.cssselect("span.Stazione")[0];
    station_name = station_name_element.text_content();
    station_red_element = el.cssselect("span.Red")[0];
    info_string = station_red_element.text_content();
    int_list = re.findall(r'\d+',info_string)    
    #print int_list
    data = {      
        'stazione': station_name,      
        'bici_libere' : int(int_list[0]),     
        'posti_disponibili' : int(int_list[1]),
        'data_ora' : now
    }
    scraperwiki.sqlite.save(unique_keys=['stazione','data_ora'], data=data)