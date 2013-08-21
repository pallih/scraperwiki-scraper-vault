import scraperwiki
from lxml.html import parse
import urllib

# Blank Python
html = urllib.urlopen("http://www.jucesponline.sp.gov.br/ResultadoBusca.aspx?ppe=CARSEG+CORRETORA+DE+SEGUROS+S%2FC.+LTDA.")

def busca(empresa):
    base_url = "http://www.jucesponline.sp.gov.br/ResultadoBusca.aspx?"
    url = base_url + urllib.urlencode({"ppe" : empresa})
    html = parse(url).getroot()
    
    tabela = html.cssselect("th[abbr=NIRE]")[0].getparent().getparent()
    for row in tabela:
        if row.cssselect("th"):
            pass
        else:
            data = {}
            data['nire'] = row.cssselect("td.item01 a")[0].text
            data['empresa'] = row.cssselect("td.item02 span")[0].text
            data['municipio'] = row.cssselect("td.item03")[0].text
            scraperwiki.sqlite.save(["nire"], data)


def getDetalhes(nire):
    base_url = "http://www.jucesponline.sp.gov.br/Pre_Visualiza.aspx?nire="
    url = base_url + str(nire)
    html = parse(url).getroot()
    print html.text_content()
    data = {}
    data['nire'] = nire
    data['tipo_sociedade'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblDetalhes")[0].text
    data['data_constituicao'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblConstituicao")[0].text
    data['data_inicio_atividades'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblAtividade")[0].text
    data['cnpj'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblCnpj")[0].text
    data['inscricao_estadual'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblInscricao")[0].text
    data['objeto'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblObjeto")[0].text_content()
    data['capital'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblCapital")[0].text
    data['endereco_logradouro'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblLogradouro")[0].text
    data['endereco_numero'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblNumero")[0].text
    data['endereco_bairro'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblBairro")[0].text
    data['endereco_complemento'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblCep")[0].text
    data['endereco_cep'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblComplemento")[0].text
    data['municipio'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblCep")[0].text
    data['uf'] = html.cssselect("#ctl00_cphContent_frmPreVisualiza_lblUf")[0].text
    scraperwiki.sqlite.save(["nire"], data)

busca("CODEP CIA. DE DESENVOLVIMENTO")
#getDetalhes(352096660123)
