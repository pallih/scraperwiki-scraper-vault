import scraperwiki
import lxml.html 

scraperwiki.sqlite.execute("delete from swdata")
html = scraperwiki.scrape("http://www.chitramala.in/news-tollywood/")
root = lxml.html.fromstring(html)
c=0
for tr in root.cssselect("div.post"):
    c=c+1
    root1=lxml.html.fromstring(lxml.html.tostring(tr))
    title=root1.cssselect("a.in_headline_title_news_inn")
    img=root1.cssselect("img.npr_img")
    desc=root1.cssselect("span.Short_Description_Style")
    data={
            'index':c,
            'title':title[0].text,
            'site':title[0].attrib['href'],
            'image':"http://www.chitramala.in"+img[0].attrib['src'],
            'source':"Chitramala",
            'detail':desc[0].text
        }
    scraperwiki.sqlite.save(unique_keys=['index'], data=data)