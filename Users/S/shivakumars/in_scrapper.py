import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.indiaglitz.com/channels/tamil/articles.asp")
root = lxml.html.fromstring(html)
node=root.cssselect("td.black")
scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("h2 a");
    node2=root1.cssselect("a img");
    node3=root1.cssselect("a.grey");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].text,
            'site':"http://www.indiaglitz.com" + node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"Indiaglitz",
            'detail':node2[0].tail
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
    
    
    


import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.indiaglitz.com/channels/tamil/articles.asp")
root = lxml.html.fromstring(html)
node=root.cssselect("td.black")
scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("h2 a");
    node2=root1.cssselect("a img");
    node3=root1.cssselect("a.grey");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].text,
            'site':"http://www.indiaglitz.com" + node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"Indiaglitz",
            'detail':node2[0].tail
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
    
    
    


