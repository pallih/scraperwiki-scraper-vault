import scraperwiki
import lxml.html           
from lxml.html.clean import clean_html


data = {'provincia': "milano", 'venditore': 'xyz'}

for i in range(1,5):   
    html = scraperwiki.scrape("http://www.assimoco.com/assimocointernet/come_trovarci/rete_vendita.jsp?cmdProvincia="+str(i))
    root = lxml.html.fromstring(html)
    prov = root.cssselect("select#cmdProvincia option")[i] 
    data['provincia'] = prov.text
    for el in root.cssselect("td.domanda"): 
        data['venditore'] = el.text
        scraperwiki.sqlite.save(['Provincia','Venditori'],{'Provincia':data['provincia'], 'Venditori':data['venditore']})





