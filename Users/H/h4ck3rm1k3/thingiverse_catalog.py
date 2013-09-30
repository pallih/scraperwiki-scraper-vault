import scraperwiki
import lxml.html           

scraperwiki.sqlite.execute("create table  if not exists categories ('name' string)")

def all_categories() :
    #names = []
    # all categories http://www.thingiverse.com/categories/
    categories_html = scraperwiki.scrape("http://www.thingiverse.com/categories/")
    #print categories_html

    #<li><a href="/tools/category:4">Automated&nbsp;Tools</a></li>
    root = lxml.html.fromstring(categories_html)
    for div in root.cssselect("div[class='category-image']"):        
        for a in div.cssselect("a"):        
            href= a.attrib['href']
            (nada,cat,name)=href.split('/')
            scraperwiki.sqlite.execute("insert into categories values (?)", array(name))

            #names.append(name)

    #print names
    scraperwiki.sqlite.commit()    

#<div class="category-image">
#<a href="/categories/3d-printing">



# one category 
# http://www.thingiverse.com/categories/3d-printing

#one item :
#  http://www.thingiverse.com/thing:27376



all_categories()import scraperwiki
import lxml.html           

scraperwiki.sqlite.execute("create table  if not exists categories ('name' string)")

def all_categories() :
    #names = []
    # all categories http://www.thingiverse.com/categories/
    categories_html = scraperwiki.scrape("http://www.thingiverse.com/categories/")
    #print categories_html

    #<li><a href="/tools/category:4">Automated&nbsp;Tools</a></li>
    root = lxml.html.fromstring(categories_html)
    for div in root.cssselect("div[class='category-image']"):        
        for a in div.cssselect("a"):        
            href= a.attrib['href']
            (nada,cat,name)=href.split('/')
            scraperwiki.sqlite.execute("insert into categories values (?)", array(name))

            #names.append(name)

    #print names
    scraperwiki.sqlite.commit()    

#<div class="category-image">
#<a href="/categories/3d-printing">



# one category 
# http://www.thingiverse.com/categories/3d-printing

#one item :
#  http://www.thingiverse.com/thing:27376



all_categories()