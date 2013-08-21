import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.kollyinsider.com/search/label/?max-results=10")
root = lxml.html.fromstring(html)
node=root.cssselect("div.post")
#scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    root2=root1.cssselect("h1");
    root2=root2[0].getnext();
    node1=root1.cssselect("h1 a");
    node2=root1.cssselect("img");
    node4=root2.cssselect("div");
    #print node4[2].tail
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].text,
            'site': node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"KollyInsider",
            'detail':node4[2].tail,
            'sourceSiteType':'IMAGE',
            'sourceUrl':'http://www.kollyinsider.com/',
            'sourceLogo':'https://lh3.googleusercontent.com/-Rwt3G0n2vZw/UJXie_bCikI/AAAAAAAAAZ4/IFzuVFJroIQ/h185/ki-glow2.png'
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)



