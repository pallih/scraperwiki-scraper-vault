import scraperwiki
import lxml.html
c=[135,144,87,110,151,147,138,131,127,122,117,108,102,90,57,41,13,150,143,137,130,126,121,116,107,100,85,54,34,9,149,141,134,129,124,120,111,106,99,61,49,33,7,148,140,133,128,123,118,109,103,98,58,48,14]
b=0
tipos=str
nombre=str
while b != 55: 
    html=scraperwiki.scrape("http://funkalab.com/collections/"+str(c[b]))
    root=lxml.html.fromstring(html)
    tipos=html.count('data-placement')
    for el in root.cssselect("h1"):
        nombre=el.text
    video=html.count('class="label">Video')
    arte=html.count('class="label">Arte')
    musica=html.count('class="label">M')
    tec=html.count('class="label">Tec')
    diseno=html.count('class="label">Dis')
    scraperwiki.sqlite.save(unique_keys=['id'],data={'id':c[b],'nombre':nombre,'video':video,'arte':arte,'musica':musica,'tec':tec,'diseno':diseno,'tipos':tipos})
    b=b+1



import scraperwiki
import lxml.html
c=[135,144,87,110,151,147,138,131,127,122,117,108,102,90,57,41,13,150,143,137,130,126,121,116,107,100,85,54,34,9,149,141,134,129,124,120,111,106,99,61,49,33,7,148,140,133,128,123,118,109,103,98,58,48,14]
b=0
tipos=str
nombre=str
while b != 55: 
    html=scraperwiki.scrape("http://funkalab.com/collections/"+str(c[b]))
    root=lxml.html.fromstring(html)
    tipos=html.count('data-placement')
    for el in root.cssselect("h1"):
        nombre=el.text
    video=html.count('class="label">Video')
    arte=html.count('class="label">Arte')
    musica=html.count('class="label">M')
    tec=html.count('class="label">Tec')
    diseno=html.count('class="label">Dis')
    scraperwiki.sqlite.save(unique_keys=['id'],data={'id':c[b],'nombre':nombre,'video':video,'arte':arte,'musica':musica,'tec':tec,'diseno':diseno,'tipos':tipos})
    b=b+1



