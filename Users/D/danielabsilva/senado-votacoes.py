import scraperwiki
import urllib
from lxml import etree

def pega_dados_votacao(cod_mat, prefix):
    contador = 0
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
        for Votacao in Votacoes.xpath(".//Votacao"):
            data = data_materia
            data["codigo_tramitacao"] = Votacao.xpath(".//CodigoTramitacao")[0].text
            data["descricao_votacao"] = Votacao.xpath(".//DescricaoVotacao")[0].text
            data["resultado"] = Votacao.xpath(".//Resultado")[0].text
            for Votos in Votacao.xpath(".//Votos"):
                for VotoParlamentar in Votos.xpath(".//VotoParlamentar"):
                    data["codigo_parlamentar"] =  VotoParlamentar.xpath(".//CodigoParlamentar")[0].text
                    data["nome_parlamentar"] = VotoParlamentar.xpath(".//NomeParlamentar")[0].text
                    data["voto"] = VotoParlamentar.xpath(".//Voto")[0].text
                    data["id"] = str(prefix) + "/" + str(contador)
                    scraperwiki.sqlite.save(["id"], data, table_name="votos_senado")
                    contador = contador + 1

prefix = 0
for item in ["100475","40941", "88022"]:
    prefix = prefix + 1
    print "Abrindo URL" + str(item)
    pega_dados_votacao(item, prefix)import scraperwiki
import urllib
from lxml import etree

def pega_dados_votacao(cod_mat, prefix):
    contador = 0
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
        for Votacao in Votacoes.xpath(".//Votacao"):
            data = data_materia
            data["codigo_tramitacao"] = Votacao.xpath(".//CodigoTramitacao")[0].text
            data["descricao_votacao"] = Votacao.xpath(".//DescricaoVotacao")[0].text
            data["resultado"] = Votacao.xpath(".//Resultado")[0].text
            for Votos in Votacao.xpath(".//Votos"):
                for VotoParlamentar in Votos.xpath(".//VotoParlamentar"):
                    data["codigo_parlamentar"] =  VotoParlamentar.xpath(".//CodigoParlamentar")[0].text
                    data["nome_parlamentar"] = VotoParlamentar.xpath(".//NomeParlamentar")[0].text
                    data["voto"] = VotoParlamentar.xpath(".//Voto")[0].text
                    data["id"] = str(prefix) + "/" + str(contador)
                    scraperwiki.sqlite.save(["id"], data, table_name="votos_senado")
                    contador = contador + 1

prefix = 0
for item in ["100475","40941", "88022"]:
    prefix = prefix + 1
    print "Abrindo URL" + str(item)
    pega_dados_votacao(item, prefix)