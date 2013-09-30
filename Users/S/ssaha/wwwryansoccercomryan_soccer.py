import scraperwiki
import lxml.html
record={}
html = scraperwiki.scrape("http://www.ryansoccer.com/Ryan_Soccer/Home.html")
root = lxml.html.fromstring(html)
for el in root.cssselect(".tinyText img"):
            record["url"]="http://www.ryansoccer.com/Ryan_Soccer/"+el.attrib['src']
            scraperwiki.sqlite.save(["url"], record)
            #print "http://www.conestogasoccer.com/gallery/"+el.attrib['src']