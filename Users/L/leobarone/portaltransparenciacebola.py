import scraperwiki
from lxml.html import parse

url = 'http://www.portaldatransparencia.gov.br/PortalTransparenciaPesquisaFavorecidoPJ_3.asp?Exercicio=2010&hidIdTipoFavorecido=2&hidNumCodigoTipoNaturezaJuridica=3&textoPesquisa=&CpfCnpjNis=61189445000156&NomeFavorecido=FUNDACAO%20BUTANTAN&valorFavorecido=91232360916&valorNatJud=&valorAcao=220768000&nomeAcao=Fomento%20a%20Projetos%20de%20Implanta%E7%E3o%20e%20Recupera%E7%E3o%20da%20Infra-Estrutura%20de%20Pesquisa%20das%20Institui%E7%F5es%20P%FAblicas%20%28CT-Infra%29&codigoAcao=2095&idFuncionalProgramatica=1361'

lista= parse(url).getroot()

for tr in lista.cssselect('href')
    
    amz = lista.cssselect('href')
    
    ps = parse(amz).getroot
   
          
        for tr in ps.cssselect('#listagemConvenios'):
            
            data = {}
            
            data['convenio'] = ps.cssselect('strong')[0].text_content()
            data['situacao'] = ps.cssselect('strong')[1].text_content()
            data['numoriginal'] = ps.cssselect('strong')[2].text_content()
            data['objetoconvenio'] = ps.cssselect('strong')[3].text_content()
            data['orgaosuperior'] = ps.cssselect('strong')[4].text_content()
            data['concedente'] = ps.cssselect('strong')[5].text_content()
            data['convenente'] = ps.cssselect('strong')[6].text_content()
            data['valorconvenio'] = ps.cssselect('strong')[7].text_content()
            data['valorliberado'] = ps.cssselect('strong')[8].text_content()
            data['publicacao'] = ps.cssselect('strong')[9].text_content()
            data['iniciovigencia'] = ps.cssselect('strong')[10].text_content()
            data['fimvigencia'] = ps.cssselect('strong')[11].text_content()
            data['valorcontrapartida'] = ps.cssselect('strong')[12].text_content()
            data['dataultimaliberacao'] = ps.cssselect('strong')[13].text_content()
            data['valorultimaliberacao'] = ps.cssselect('strong')[14].text_content()
        
            print data
            scraperwiki.sqlite.save(['convenio'], data)