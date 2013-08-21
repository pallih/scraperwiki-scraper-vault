import scraperwiki
import lxml.html

#url = "http://scraperwikiviews.com/run/python_lxml_cheat_sheet/"
url = "http://www.skl.se/kommuner_och_landsting/om_kommuner/kommuner?searchtype=all"

root = lxml.html.parse(url).getroot()
#print lxml.html.tostring(root)

# all paragraphs with class="kkk"
kommuner = root.cssselect("div.Text")

#print paras
#Aneby kommun
#Box 53
#57822 ANEBY
#Tfn: 0380-46100
#Fax: 0380-46195
#E-post: aneby.kommun@aneby.se

for k in kommuner:
    c = k.getchildren()
    if len(c) == 5:
        data = {"name": c[0].cssselect("a")[0].text, "url": c[0].cssselect("a")[0].attrib.get("href"), "adress": c[1].text, "epost": c[4].cssselect("a")[0].text }
        
        scraperwiki.sqlite.save(unique_keys=["url"], data=data)

    

