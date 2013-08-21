import scraperwiki
import lxml.html           

scraperwiki.sqlite.execute("create table  if not exists sub_categories ('parent' string, 'name' string)")

def sub_categories(parent) :
    sub_cat_html = scraperwiki.scrape("http://www.thingiverse.com/categories/%s" % parent)
    root = lxml.html.fromstring(sub_cat_html)

    for div in root.cssselect("div[class='category-image']"):        
        for a in div.cssselect("a"):        
            href= a.attrib['href']
            (nada,cat,name)=href.split('/')
            scraperwiki.sqlite.execute("insert into sub_categories values (?,?)", (parent,name))
    scraperwiki.sqlite.commit()    



sub_categories("3d-printing")


#<a href="/categories/3d-printing/page:81"><img src="/img/pagination/last.gif" alt="Last"></a>