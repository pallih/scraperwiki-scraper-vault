import scraperwiki
import lxml.html
a=['http://www.bolivianexpress.org/blog/posts/go-gringo-go',
'http://www.bolivianexpress.org/blog/posts/luces-camara-accion',
'http://www.bolivianexpress.org/blog/posts/moving-mountains',
'http://www.bolivianexpress.org/blog/posts/invisible-heroes',
'http://www.bolivianexpress.org/blog/posts/we-ll-have-a-gay-old-time',
'http://www.bolivianexpress.org/blog/posts/hanging-out-with-the-lustrabotas',
'http://www.bolivianexpress.org/blog/posts/tall-white-and-english-speaking',
'http://www.bolivianexpress.org/blog/posts/recuperar-recuperar-el-litoral-y-el-ancho-mar']
b=0
while b!=4:
    html=scraperwiki.scrape(str(a[b]))
    root=lxml.html.fromstring(html)
    count=len(str(html))
    #for el in root.cssselect("article"):
        #count=len(str(el.text))
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'count':count,'id':str(a[b])})
    b=b+1
import scraperwiki
import lxml.html
a=['http://www.bolivianexpress.org/blog/posts/go-gringo-go',
'http://www.bolivianexpress.org/blog/posts/luces-camara-accion',
'http://www.bolivianexpress.org/blog/posts/moving-mountains',
'http://www.bolivianexpress.org/blog/posts/invisible-heroes',
'http://www.bolivianexpress.org/blog/posts/we-ll-have-a-gay-old-time',
'http://www.bolivianexpress.org/blog/posts/hanging-out-with-the-lustrabotas',
'http://www.bolivianexpress.org/blog/posts/tall-white-and-english-speaking',
'http://www.bolivianexpress.org/blog/posts/recuperar-recuperar-el-litoral-y-el-ancho-mar']
b=0
while b!=4:
    html=scraperwiki.scrape(str(a[b]))
    root=lxml.html.fromstring(html)
    count=len(str(html))
    #for el in root.cssselect("article"):
        #count=len(str(el.text))
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'count':count,'id':str(a[b])})
    b=b+1
