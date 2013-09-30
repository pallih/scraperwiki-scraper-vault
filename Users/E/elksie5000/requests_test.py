import scraperwiki
import requests
import lxml.html
import re


url = "http://www.stoke.gov.uk/ccm/content/xml-feeds/licensing/licensing---view-public-register.en?bbp.s=1&form.licensing---view-public-register=visited&bbp.i=d0.1&pname=&aname=&pcode=&lno=&ltype=Premise%20Licences"

r = requests.get(url)

root_content = r.content

#print root_content
root = lxml.html.fromstring(root_content)
index = 0
links = root.cssselect("div.sodresult div.sodresultleft div#containersod a")
for link in links:
    
    detail = link.attrib.get('href')
    html = scraperwiki.scrape(detail)
    root = lxml.html.fromstring(html)
    container = root.cssselect("div.sodresult div.sodresultleft div#containersod")
    #if container[0] isn't empty split, otherwise move on 
    if container:
        index += 1
        #print lxml.html.tostring(container[0])
        container_string = lxml.html.tostring(container[0])
        container_str = container_string.strip()
        #print container_str
        
        strongstart_txt = "<strong>"
        strongend_txt = "</strong>"
        break_txt = "<br>"
        strongbreak_txt = "<br><strong>"
        entities = container_str.count(strongend_txt)
        record = {}
        
        for el in range(entities):
            name_bit = container_str[(container_str.find(strongstart_txt)+strongstart_txt.__len__()):container_str.find(strongend_txt)] 
            name_part = name_bit.replace("Date\n                           Received ", "Date Received")
            name_part = name_part.replace("Premises\n                           Name ", "Premises Name")
            name_part = name_part.replace("Status\n                           ", "Status")
            name_part = name_part.replace("Premises Address\n                           ", "Premises Address")
            name_part = name_part.replace("Licence\n                           Starts ", "Licence Starts")
            name_part = name_part.replace("Premises\n                           Address ", "Premises Address")
            #print name_part
            print index
            record['index'] = index
            container_str =container_str[(container_str.find(strongend_txt)+strongend_txt.__len__()):]    
            data_bit = container_str[:container_str.find(strongbreak_txt)]
            data_bit = data_bit.replace("<br>", "") 
            data_part2 = data_bit.replace("</div", "")
            data_part = data_part2.lstrip(", ")
            #print data_part
            container_str = container_str[(container_str.find(strongbreak_txt)):]
            record[name_part] = data_part
    
        #print record
        scraperwiki.sqlite.save(['index'], record)
        import scraperwiki
import requests
import lxml.html
import re


url = "http://www.stoke.gov.uk/ccm/content/xml-feeds/licensing/licensing---view-public-register.en?bbp.s=1&form.licensing---view-public-register=visited&bbp.i=d0.1&pname=&aname=&pcode=&lno=&ltype=Premise%20Licences"

r = requests.get(url)

root_content = r.content

#print root_content
root = lxml.html.fromstring(root_content)
index = 0
links = root.cssselect("div.sodresult div.sodresultleft div#containersod a")
for link in links:
    
    detail = link.attrib.get('href')
    html = scraperwiki.scrape(detail)
    root = lxml.html.fromstring(html)
    container = root.cssselect("div.sodresult div.sodresultleft div#containersod")
    #if container[0] isn't empty split, otherwise move on 
    if container:
        index += 1
        #print lxml.html.tostring(container[0])
        container_string = lxml.html.tostring(container[0])
        container_str = container_string.strip()
        #print container_str
        
        strongstart_txt = "<strong>"
        strongend_txt = "</strong>"
        break_txt = "<br>"
        strongbreak_txt = "<br><strong>"
        entities = container_str.count(strongend_txt)
        record = {}
        
        for el in range(entities):
            name_bit = container_str[(container_str.find(strongstart_txt)+strongstart_txt.__len__()):container_str.find(strongend_txt)] 
            name_part = name_bit.replace("Date\n                           Received ", "Date Received")
            name_part = name_part.replace("Premises\n                           Name ", "Premises Name")
            name_part = name_part.replace("Status\n                           ", "Status")
            name_part = name_part.replace("Premises Address\n                           ", "Premises Address")
            name_part = name_part.replace("Licence\n                           Starts ", "Licence Starts")
            name_part = name_part.replace("Premises\n                           Address ", "Premises Address")
            #print name_part
            print index
            record['index'] = index
            container_str =container_str[(container_str.find(strongend_txt)+strongend_txt.__len__()):]    
            data_bit = container_str[:container_str.find(strongbreak_txt)]
            data_bit = data_bit.replace("<br>", "") 
            data_part2 = data_bit.replace("</div", "")
            data_part = data_part2.lstrip(", ")
            #print data_part
            container_str = container_str[(container_str.find(strongbreak_txt)):]
            record[name_part] = data_part
    
        #print record
        scraperwiki.sqlite.save(['index'], record)
        