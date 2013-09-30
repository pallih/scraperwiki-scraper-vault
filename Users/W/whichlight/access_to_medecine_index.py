import scraperwiki 
import lxml.html           
import re
        
html = scraperwiki.scrape("http://www.accesstomedicineindex.org/content/index-2010-0")
root = lxml.html.fromstring(html) 
data = {}

table = root.cssselect("tbody")[0]
for tr in table.cssselect("tr"):
    for td in tr: 
        #pull name
        if (td.find_class("naam")):
            name =  td.text_content()

        for div in td:
            for d in div:
                #pull vals from div
                #get label
                labelRE = "title=.*:"
                string = lxml.html.tostring(d)
                label= re.search(labelRE, string).group(0).replace("title=\"","").replace(":","").replace("R&amp;D","RD")
                labelvalRE = labelRE + ".*\""
                numRE = ":.*\""
                value =  re.search(numRE,re.search(labelvalRE, string).group(0)).group(0).replace(": ","").replace("\"","")
                data[label]=value
    data["name"] = name

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)import scraperwiki 
import lxml.html           
import re
        
html = scraperwiki.scrape("http://www.accesstomedicineindex.org/content/index-2010-0")
root = lxml.html.fromstring(html) 
data = {}

table = root.cssselect("tbody")[0]
for tr in table.cssselect("tr"):
    for td in tr: 
        #pull name
        if (td.find_class("naam")):
            name =  td.text_content()

        for div in td:
            for d in div:
                #pull vals from div
                #get label
                labelRE = "title=.*:"
                string = lxml.html.tostring(d)
                label= re.search(labelRE, string).group(0).replace("title=\"","").replace(":","").replace("R&amp;D","RD")
                labelvalRE = labelRE + ".*\""
                numRE = ":.*\""
                value =  re.search(numRE,re.search(labelvalRE, string).group(0)).group(0).replace(": ","").replace("\"","")
                data[label]=value
    data["name"] = name

    scraperwiki.sqlite.save(unique_keys=['name'], data=data)