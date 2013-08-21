import scraperwiki
import lxml.html
#Required Nodes look like this
#<li><a>name</a><a>city/town</a><a>county</a>state</li>
#or with a sub UL. Want all LI items that conform to structure.
#<li><a>name</a><a>city/town</a><a>county</a>state<ul><li><a>name</a><a>city/town</a><a>county</a>state</li>...</ul></li>


url = "http://www.ushospital.info/Texas.htm"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html) 

#This does nto work yet.
li = root.findall(".//li")
for l in li:
    #Here need to recognise the patterns given above and extract the data.
    print l.text
    #build a list of objects with the right pattern.
    #hospital = {"name"=name,"url"=url-from-first-anchor","city"=city ...}
    #scraperwiki.sqlite.save(unique_keys=['name',], data=data)

#Then we can use this to get a nice clean CSV
