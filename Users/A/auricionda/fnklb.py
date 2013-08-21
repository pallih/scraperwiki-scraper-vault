import scraperwiki
import lxml.html
c=[5,6,14,20,27,29,37,43,50,92,96,99,101,102,103,108,113,114,115,116,118,119,149,153,159,165,170,171,172,177,178,190,204,207,230,249,253,256,270,279,302,308,316,4,15,18,26,31,32,162]
b=0
label=str
i=1
creados=int
while b != 50: 
    html=scraperwiki.scrape("http://funkalab.com/users/"+str(c[b]))
    root=lxml.html.fromstring(html)
    for el in root.cssselect("h1 small"):
        ciudad=el.text
    for el in root.cssselect("h3"):
        descrip=el.text
    for el in root.cssselect("span.label-info"):
        if i==1:
            label1=el.text
            i=i+1
        else:
            label2=el.text
            i=1
    creados=html.count('board-thumb')
    scraperwiki.sqlite.save(unique_keys=['id'],data={'id':c[b],'ciudad':ciudad,'descrip':descrip,'label1':label1,'label2':label2,'creados':creados})
    b=b+1

