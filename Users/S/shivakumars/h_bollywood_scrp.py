import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://bollywood.celebden.com/category/bollywood-news/")
root = lxml.html.fromstring(html)
node=root.cssselect("div.home_post_cont.post_box")
#scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("a");
    node2=root1.cssselect("a img");
    #node3=root1.cssselect("h4 a");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].attrib['title'],
            'site': node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"Bollywood Celeden",
            'detail':"Click For More",
            'sourceSiteType':'IMAGE',
            'sourceUrl':'http://bollywood.celebden.com/',
            'sourceLogo':'http://bollywoodimages.celebden.com/themes/gridthemeresponsive/images/bollywood_celebden_logo.png'
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://bollywood.celebden.com/category/bollywood-news/")
root = lxml.html.fromstring(html)
node=root.cssselect("div.home_post_cont.post_box")
#scraperwiki.sqlite.execute("delete from swdata");
c=0
for i in node:
    c=c+1
    #print lxml.html.tostring(i)
    root1=lxml.html.fromstring(lxml.html.tostring(i))
    node1=root1.cssselect("a");
    node2=root1.cssselect("a img");
    #node3=root1.cssselect("h4 a");
    if len(node1)>=1 :
        data={
            'index':c,
            'title':node1[0].attrib['title'],
            'site': node1[0].attrib['href'],
            'image':node2[0].attrib['src'],
            'source':"Bollywood Celeden",
            'detail':"Click For More",
            'sourceSiteType':'IMAGE',
            'sourceUrl':'http://bollywood.celebden.com/',
            'sourceLogo':'http://bollywoodimages.celebden.com/themes/gridthemeresponsive/images/bollywood_celebden_logo.png'
        }
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)