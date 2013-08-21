import scraperwiki
import lxml.html
a=[2369,2337,377,2364,1764]
b=3
while b!=5:
    c=['brasil','usa','mexico','venezuela','argentina','colombia','chile','peru','puerto_rico','panama','elsalvador','uruguay','guatemala','ecuador','nicaragua','bolivia']
    d=0
    while d!=16:
        html = scraperwiki.scrape("http://amerpages.com/spa/"+str(c[d])+"/items/search/category:"+str(a[b]))
        root = lxml.html.fromstring(html)
        for el in root.cssselect("div.resultsInfo strong"):
            if el.text != 'Ordenar por:':
                categoria=int(el.text)
        f=html.count('listing featured')
        if d==0:
            brasilc=categoria
            brasilf=f
        if d==1:
            usac=categoria
            usaf=f  
        if d==2:
            mexicoc=categoria
            mexicof=f
        if d==3:
            venezuelac=categoria
            venezuelaf=f
        if d==4:
            argentinac=categoria
            argentinaf=f
        if d==5:
            colombiac=categoria
            colombiaf=f
        if d==6:
            chilec=categoria
            chilef=f
        if d==7:
            peruc=categoria
            peruf=f
        if d==8:
            puerto_ricoc=categoria
            puerto_ricof=f
        if d==9:
            panamac=categoria
            panamaf=f
        if d==10:
            elsalvadorc=categoria
            elsalvadorf=f
        if d==11:
            uruguayc=categoria
            uruguayf=f
        if d==12:
            guatemalac=categoria
            guatemalaf=f
        if d==13:
            ecuadorc=categoria
            ecuadorf=f  
        if d==14:
            nicaraguac=categoria
            nicaraguaf=f 
        if d==15:
            boliviac=categoria
            boliviaf=f  
        for el in root.cssselect("h1.mainTitle"):
            titulo=el.text
        d=d+1
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'titulo':titulo,'codigo':a[b],'brasilc':brasilc,'brasilf':brasilf,'usac':usac,'usaf':usaf,'mexicoc':mexicoc,'mexicof':mexicof,'venezuelac':venezuelac,'venezuelaf':venezuelaf,'argentinac':argentinac,'argentinaf':argentinaf,'colombiac':colombiac,'colombiaf':colombiaf,'chilec':chilec,'chilec':chilef,'peruc':peruc,'peruf':peruf,'puerto_ricoc':puerto_ricoc,'puerto_ricof':puerto_ricof,'panamac':panamac,'panamaf':panamaf,'elsalvadorc':elsalvadorc,'elsalvadorf':elsalvadorf,'uruguayc':uruguayc,'uruguayf':uruguayf,'guatemalac':guatemalac,'guatemalaf':guatemalaf,'nicaraguac':nicaraguac,'nicaraguaf':nicaraguaf,'boliviac':boliviac,'boliviaf':boliviaf},table_name='pago',verbose=2)
    b=b+1
