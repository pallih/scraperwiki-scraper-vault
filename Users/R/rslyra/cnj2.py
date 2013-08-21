###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
i2=0

for i in xrange(2):
    #print "=============================="
    i1=i+0

    print i1
    html = scraperwiki.scrape('http://www.cnj.jus.br/cna/Controle/ConsultaPublicaBuscaControle.php?transacao=CONSULTA&vara=%d'%i1)
    #print html

    from BeautifulSoup import BeautifulSoup
    soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
    tds = soup.findAll('td') # get all the <td> tags
    #print tds

    i2=i2+1
    dados = {}
    dados['id']= i2
    dados['texto']= i
    scraperwiki.sqlite.save(['id'],dados) # save the records one by one


    for td in tds:
        #print td.text
        #if  (td.text != '') and (td.text != 'VARA:') and (td.text != 'Endereço:') and (td.text != 'Bairro:') and (td.text != 'Resultado da pesquisa') :
        i2=i2+1
        dados = {}
        dados['id']= i2
        dados['texto']= td.text  # just the text inside the HTML tag
        scraperwiki.sqlite.save(['id'],dados) # save the records one by one
