import scraperwiki
import lxml.html
import lxml.etree
import datetime

root = lxml.html.parse('http://www.lavoz.com.ar/horoscopo').getroot()
signos = root.cssselect("div.Prediccion")

date = datetime.datetime.now().strftime("%Y-%m-%d")
datos = {}
for s in signos:
    prediccion = {}
    l = list(s)
    signo = l[0].text_content()
    nacidos = l[1].text_content()
    t = l[2].text_content()
    consejo,r = t.split('Amor: ')
    amor,r = r.split('Riqueza: ')
    riqueza,bienestar = r.split('Bienestar: ')
    prediccion.update({'consejo':consejo})
    prediccion.update({'amor':amor})
    prediccion.update({'riqueza':riqueza})
    prediccion.update({'bienestar':bienestar})
    datos.update({signo:prediccion})
    print signo
    print prediccion

for signo in datos:
    p = datos[signo]
    record = {'signo':signo, 
        'consejo':p['consejo'], 
        'amor':p['amor'], 
        'riqueza':p['riqueza'],
        'bienestar':p['bienestar'],
        'date':date } 
    scraperwiki.sqlite.save(['signo','date'],record)
    
