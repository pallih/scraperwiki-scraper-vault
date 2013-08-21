import scraperwiki
from lxml.html import parse

base_url = "http://www.al.sp.gov.br/spl_consultas/consultaProposicoesAction.do?direction=inicio&lastPage=0&currentPage=0&act=detalhe&idDocumento=&rowsPerPage=500&tpDocumento=&method=search&text=&natureId=4005&legislativeNumber=&legislativeYear=&natureIdMainDoc=loa&anoDeExercicio=2011&legislativeNumberMainDoc=&legislativeYearMainDoc=&strInitialDate=&strFinalDate=&author=&supporter=&politicalPartyId=&stageId=&strVotedInitialDate=&strVotedFinalDate=&approved=&rejected=&advancedSearch=&currentPageDetalhe="

#url = "teste.html"

def main():
  for i in range(0,3):
    print 'Getting page ' + str(i)
    getEmendas(base_url+str(i))

def test():
    getEmendas('http://hacks.thomaslevine.com/consultaProposicoesAction.do.html')

def getEmendas(url):
    html = parse(url) #.getroot()
    rows = html.xpath('//tr[td[@width="320"]]')

    for row in rows:
        cell = row.cssselect("td")
        emenda = {}
        emenda['data'] = cell[0].text_content()
        emenda['titulo'] = cell[1].cssselect("b")[0].text_content()
        emenda['descricao'] = cell[1].xpath("//a")[0].text_content()
        emenda['parlamentar'] = cell[2].text_content()
        emenda['etapa'] = cell[3].text_content()
        scraperwiki.sqlite.save(["titulo"], emenda)

main()