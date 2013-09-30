import scraperwiki
import lxml.html
record={}
html = scraperwiki.scrape("http://stoganews.com/news/")
root = lxml.html.fromstring(html)
for el in root.cssselect("img.alignleft"):
            link=el.attrib['src']
            link=link.replace("%3A",":")
            link=link.replace("%2F","/")
            anew=link.split("src=")
            #alink=anew[1].split("&")
            record["url"]=anew
            scraperwiki.sqlite.save(["url"], record)
            print anew[0]
