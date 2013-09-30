import scraperwiki
import urllib
from lxml import etree

#DetalheMateria
#Materias
#Votacoes
#Votacao
    #CodigoTramitacao
    #DescricaoVotacao
    #Resultado

#Votos
    #CodigoParlamentar
    #NomeParlamentar
    #Voto
    

def pega_dados_votacao(cod_mat):
    url_xml = "http://legis.senado.gov.br/dadosabertos/materia/" + str(cod_mat)
    xml = urllib.urlopen(url_xml).read()
    root = etree.fromstring(xml)
    for Materias in root.xpath(".//Materias"):
        for Materia in root.xpath(".//Materia"):
            data_materia = {}
            data_materia["codigo"] = str(cod_mat)
            data_materia["subtipo"] = Materia.xpath(".//Subtipo")[0].text
            data_materia["descricao_subtipo"] = Materia.xpath(".//DescricaoSubtipo")[0].text
            data_materia["numero"] = Materia.xpath(".//Numero")[0].text
            data_materia["ano"] = Materia.xpath(".//Ano")[0].text
            data_materia["data_apresentacao"] = Materia.xpath(".//DataApresentacao")[0].text
            data_materia["ementa"] = Materia.xpath(".//Ementa")[0].text
    for Votacoes in root.xpath(".//Votacoes"):
        for Votacao in root.xpath(".//Votacao"):
            data = data_materia
            data["codigo_tramitacao"] = Votacao.xpath(".//CodigoTramitacao")[0].text
            data["descricao_votacao"] = Votacao.xpath(".//DescricaoVotacao")[0].text
            data["resultado"] = Votacao.xpath(".//Resultado")[0].text
            for Votos in Votacao.xpath(".//Votos"):
                for VotoParlamentar in Votos.xpath(".//VotoParlamentar"):
                    data["codigo_parlamentar"] =  VotoParlamentar.xpath(".//CodigoParlamentar")[0].text
                    data["nome_parlamentar"] = VotoParlamentar.xpath(".//NomeParlamentar")[0].text
                    data["voto"] = VotoParlamentar.xpath(".//Voto")[0].text
                    scraperwiki.sqlite.save(["codigo_parlamentar"], data, table_name="votos_senado")
    

pega_dados_votacao("100475")import scraperwiki
import urllib
from lxml import etree

#DetalheMateria
#Materias
#Votacoes
#Votacao
    #CodigoTramitacao
    #DescricaoVotacao
    #Resultado

#Votos
    #CodigoParlamentar
    #NomeParlamentar
    #Voto
    

def pega_dados_votacao(cod_mat):
    url_xml = "http://legis.senado.gov.br/dadosabertos/materia/" + str(cod_mat)
    xml = urllib.urlopen(url_xml).read()
    root = etree.fromstring(xml)
    for Materias in root.xpath(".//Materias"):
        for Materia in root.xpath(".//Materia"):
            data_materia = {}
            data_materia["codigo"] = str(cod_mat)
            data_materia["subtipo"] = Materia.xpath(".//Subtipo")[0].text
            data_materia["descricao_subtipo"] = Materia.xpath(".//DescricaoSubtipo")[0].text
            data_materia["numero"] = Materia.xpath(".//Numero")[0].text
            data_materia["ano"] = Materia.xpath(".//Ano")[0].text
            data_materia["data_apresentacao"] = Materia.xpath(".//DataApresentacao")[0].text
            data_materia["ementa"] = Materia.xpath(".//Ementa")[0].text
    for Votacoes in root.xpath(".//Votacoes"):
        for Votacao in root.xpath(".//Votacao"):
            data = data_materia
            data["codigo_tramitacao"] = Votacao.xpath(".//CodigoTramitacao")[0].text
            data["descricao_votacao"] = Votacao.xpath(".//DescricaoVotacao")[0].text
            data["resultado"] = Votacao.xpath(".//Resultado")[0].text
            for Votos in Votacao.xpath(".//Votos"):
                for VotoParlamentar in Votos.xpath(".//VotoParlamentar"):
                    data["codigo_parlamentar"] =  VotoParlamentar.xpath(".//CodigoParlamentar")[0].text
                    data["nome_parlamentar"] = VotoParlamentar.xpath(".//NomeParlamentar")[0].text
                    data["voto"] = VotoParlamentar.xpath(".//Voto")[0].text
                    scraperwiki.sqlite.save(["codigo_parlamentar"], data, table_name="votos_senado")
    

pega_dados_votacao("100475")