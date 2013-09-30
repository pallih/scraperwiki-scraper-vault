import scraperwiki

# Blank Python

html = scraperwiki.scrape("http://www.www2.scuola.cl/category/news/")



import lxml.html           
root = lxml.html.fromstring(html)


for div in root.cssselect("div[class='blog_container']"):
    headline = div.cssselect("div[class='blog_headline']")
    content = div.cssselect("div[class='blog_excerpt']")
    data = {
        'headline' : headline[0].text_content(),
        'content' : content[0].text_content(),
    }
    print data    
    

    scraperwiki.sqlite.save(unique_keys=['headline'], data=data)