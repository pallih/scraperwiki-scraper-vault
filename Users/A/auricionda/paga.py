import scraperwiki
import lxml.html
c=['chile','ecuador']
d=0
b=0
while d != 2:
    a=[2369,2337,377,2364,1764]
    titulo=str
    while b != 5: 
        html = scraperwiki.scrape("http://amerpages.com/spa/"+str(c[d])+"/items/search/category:"+str(a[b]))
        root = lxml.html.fromstring(html)
        for el in root.cssselect("div.resultsInfo strong"):
            if el.text != 'Ordenar por:':
                categoria=int(el.text)
        f=html.count('listing featured')
        for el in root.cssselect("h1.mainTitle"):
            titulo=el.text
        scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'featured':f,'categoria':categoria,'titulo':titulo,'codigo':a[b],'pais':c[d]},table_name='paga',verbose=2)
        b=b+1
        f=0
    b=0
    d=d+1