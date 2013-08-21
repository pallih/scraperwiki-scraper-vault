import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://entertainment.oneindia.in/tamil/news/")
root = lxml.html.fromstring(html)
node=root.cssselect("div.collection")
scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("a");
    node2=root1.cssselect("a img");
    node3=root1.cssselect("h4 a");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node3[0].text,
            'site':"http://entertainment.oneindia.in" + node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"OneIndia",
            'detail':"Click For More",
            'sourceSiteType':'IMAGE',
            'sourceUrl':'http://entertainment.oneindia.in',
            'sourceLogo':'http://entertainment.oneindia.in/img/oneindia-entertainment.jpg'
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)