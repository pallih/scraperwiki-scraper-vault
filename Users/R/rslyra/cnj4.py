###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

i2=0
dados = {}

#for i in xrange(3200):
for i in xrange(6):
    #print "=============================="
    i1=i+1

    html = scraperwiki.scrape('http://www.cnj.jus.br/cna/Controle/ConsultaPublicaBuscaControle.php?transacao=CONSULTA&vara=%d'%i1)
    print i1
    print 'http://www.cnj.jus.br/cna/Controle/ConsultaPublicaBuscaControle.php?transacao=CONSULTA&vara=%d'%i1
    print html


    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
    tds = soup.findAll('td') # get all the <td> tags
    #print tds

    cont = ""
    fl1=2

    ok=1
    old="xxx"
    for td in tds:
        #if old=="Comarca:" and td.text=="":
        #    ok=0
        #    break
        cont=cont  + td.text + "@"
        old=td.text

    if ok==1:
        dados['id']= i1
        dados['texto']= cont
        scraperwiki.sqlite.save(['id'],dados) # save the records one by one

