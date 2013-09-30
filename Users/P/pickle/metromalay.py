import scraperwiki
import lxml.html 

#scraperwiki.sqlite.execute("delete from swdata")
html = scraperwiki.scrape("http://www.metromatinee.com/MalayalamMovieNews/1")
root = lxml.html.fromstring(html)
c=0
for tr in root.cssselect("div.TheatreBlockMain"):
    c=c+1
    root1=lxml.html.fromstring(lxml.html.tostring(tr))
    title=root1.cssselect("a")
    img=root1.cssselect("img")
    desc=root1.cssselect("span.NewsSingleContant a")
    data={
            'index':c,
            'title':title[1].text,
            'site':"http://www.metromatinee.com"+title[1].attrib['href'].replace("..",""),
            'image':"http://www.metromatinee.com"+img[0].attrib['src'].replace("..",""),
            'source':"Metromatine",
            'detail':desc[0].text
        }
    scraperwiki.sqlite.save(unique_keys=['index'], data=data)



import scraperwiki
import lxml.html 

#scraperwiki.sqlite.execute("delete from swdata")
html = scraperwiki.scrape("http://www.metromatinee.com/MalayalamMovieNews/1")
root = lxml.html.fromstring(html)
c=0
for tr in root.cssselect("div.TheatreBlockMain"):
    c=c+1
    root1=lxml.html.fromstring(lxml.html.tostring(tr))
    title=root1.cssselect("a")
    img=root1.cssselect("img")
    desc=root1.cssselect("span.NewsSingleContant a")
    data={
            'index':c,
            'title':title[1].text,
            'site':"http://www.metromatinee.com"+title[1].attrib['href'].replace("..",""),
            'image':"http://www.metromatinee.com"+img[0].attrib['src'].replace("..",""),
            'source':"Metromatine",
            'detail':desc[0].text
        }
    scraperwiki.sqlite.save(unique_keys=['index'], data=data)



