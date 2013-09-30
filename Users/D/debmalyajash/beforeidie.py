import scraperwiki
import lxml.html           

# Blank Python
# Get the content from the beforeidie site
html = scraperwiki.scrape("http://beforeidie.cc/site/blog/category/responses/")


# get the root of the content
root = lxml.html.fromstring(html)


dream_str = ""
count = 0
for tr in root.cssselect("div.jump-response"):
    dream_str = lxml.html.tostring(tr)
    dream_str = dream_str[dream_str.find('&#8220;', 0) + len("&#8220;"):dream_str.find("&#8221;", 0)]
    count = count + 1 
    data = {
        'recno' : count, 
        'wish' : dream_str
      
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['recno'],data=data)import scraperwiki
import lxml.html           

# Blank Python
# Get the content from the beforeidie site
html = scraperwiki.scrape("http://beforeidie.cc/site/blog/category/responses/")


# get the root of the content
root = lxml.html.fromstring(html)


dream_str = ""
count = 0
for tr in root.cssselect("div.jump-response"):
    dream_str = lxml.html.tostring(tr)
    dream_str = dream_str[dream_str.find('&#8220;', 0) + len("&#8220;"):dream_str.find("&#8221;", 0)]
    count = count + 1 
    data = {
        'recno' : count, 
        'wish' : dream_str
      
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['recno'],data=data)