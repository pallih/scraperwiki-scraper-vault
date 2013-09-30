import scraperwiki

# Blank Python

#http://www.comprasestatales.gub.uy/consultas/ConsultaComprasResultado.php?numPagina=1&numRegistro=0&numLimite=20&pCompra=c
# downloadthepage
#interpretthepage
#identify each row
# get the content of the cells
#save it to a database
for page in range (10):
#Herewearefetchingthepage
    url = "http://www.comprasestatales.gub.uy/consultas/ConsultaComprasResultado.php?" \
      + "numPagina=%s&pCompra=&nuevaConsulta=&selEstado=a&selBuscar=&selCompra=0&selTipo=0&selTipoResolucion=0" \
      + "&selCasos=todos&selInciso=0&selGrupo=0&txtFechaDesde=01%%2F01%%2F2011&txtFechaHasta=19%%2F10%%2F2011&" \
      + "txtNumeroCompra=&txtAnioCompra=&selProvTipoDoc=R&txtRUC=&buscarArtPor=fam&codArticulo=&selFamlia=0"

    html = scraperwiki.scrape(url % page)

    #parsing
    import lxml.html           
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table[id=resultados] tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    print headers
    for tr in rows[1:]:
        print lxml.html.tostring(tr)
        tds = tr.cssselect("td")
        data={
          'Request' : tds[1].text_content(),
          'Contract Object' : tds[2].text_content(),
          'Date' : tds[3].text_content().strip() }
        print data
      
        scraperwiki.sqlite.save(['Request'], data, 'requests')import scraperwiki

# Blank Python

#http://www.comprasestatales.gub.uy/consultas/ConsultaComprasResultado.php?numPagina=1&numRegistro=0&numLimite=20&pCompra=c
# downloadthepage
#interpretthepage
#identify each row
# get the content of the cells
#save it to a database
for page in range (10):
#Herewearefetchingthepage
    url = "http://www.comprasestatales.gub.uy/consultas/ConsultaComprasResultado.php?" \
      + "numPagina=%s&pCompra=&nuevaConsulta=&selEstado=a&selBuscar=&selCompra=0&selTipo=0&selTipoResolucion=0" \
      + "&selCasos=todos&selInciso=0&selGrupo=0&txtFechaDesde=01%%2F01%%2F2011&txtFechaHasta=19%%2F10%%2F2011&" \
      + "txtNumeroCompra=&txtAnioCompra=&selProvTipoDoc=R&txtRUC=&buscarArtPor=fam&codArticulo=&selFamlia=0"

    html = scraperwiki.scrape(url % page)

    #parsing
    import lxml.html           
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table[id=resultados] tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    print headers
    for tr in rows[1:]:
        print lxml.html.tostring(tr)
        tds = tr.cssselect("td")
        data={
          'Request' : tds[1].text_content(),
          'Contract Object' : tds[2].text_content(),
          'Date' : tds[3].text_content().strip() }
        print data
      
        scraperwiki.sqlite.save(['Request'], data, 'requests')