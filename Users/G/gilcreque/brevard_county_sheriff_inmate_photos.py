import scraperwiki
import lxml.html
import os

html = scraperwiki.scrape("http://www.brevardsheriff.com/dar/inmatephotos/index.html")
root = lxml.html.fromstring(html)
for inmates in root.cssselect("p.MsoNormal a"):           
    id = os.path.splitext(inmates.attrib['href'])[0]
    name = inmates.text
    photo1 = "http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-1.jpg"
    photo2 = "http://www.brevardsheriff.com/dar/inmatephotos/Images/"+id+"-2.jpg"
    report = "http://www.brevardsheriff.com/dar/inmatephotos/"+id+".html"
    scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "name":name, "photo1":photo1, "photo2":photo2, "report":report})