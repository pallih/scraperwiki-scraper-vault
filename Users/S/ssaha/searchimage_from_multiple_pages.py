import scraperwiki
import lxml.html
output = []
url=''
record={}
def uniq(input):
    if input not in output:
        output.append(input)
UniqList={}
html=scraperwiki.scrape("http://stoganews.com/")
root=lxml.html.fromstring(html)
divs=root.cssselect("div.featuredPost a")
for div in divs:
     url=div.attrib['href']
     #url=url.replace("#respond","")
     uniq(url)
for aurl in output:
    html1=scraperwiki.scrape(aurl)
    root1=lxml.html.fromstring(html1)
    ndvis=root1.cssselect('img')
    for ndiv in ndvis:
        if  ".jpg" not in ndiv.attrib["src"]: #or "uploads"
               continue
        record["url"]= ndiv.attrib["src"]
        scraperwiki.sqlite.save(["url"], record)

