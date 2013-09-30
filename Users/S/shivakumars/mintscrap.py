import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://123tamilcinema.com")
root = lxml.html.fromstring(html)
node=root.cssselect("div.post")
#scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("h2 a");
    node2=root1.cssselect("a img");
    node3=root1.cssselect("a");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].text,
            'site':node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"123tamilcinema.com",
            'detail':node3[2].tail
        }
        #print lxml.html.tostring(node3[2].tail)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)



import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://123tamilcinema.com")
root = lxml.html.fromstring(html)
node=root.cssselect("div.post")
#scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("h2 a");
    node2=root1.cssselect("a img");
    node3=root1.cssselect("a");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].text,
            'site':node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"123tamilcinema.com",
            'detail':node3[2].tail
        }
        #print lxml.html.tostring(node3[2].tail)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)



