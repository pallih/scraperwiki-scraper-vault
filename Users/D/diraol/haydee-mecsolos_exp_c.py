# -*- coding: utf-8 -*-     

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://diraol.eng.br/dee/'
experimentos = {'C':"C.html"}#{'P':"P.html"}#{'R':"R.html"}
categorias = ("turma","equipe","tipo_de_ensaio","umidade_de_compactacao","peso_especifico_aparente_seco_na_umidade_de_compactacao","indice_de_vazios_no_ponto_de_compactacao","tensao_de_ruptura_no_ponto_de_compactacao","tensao_final_no_ponto_de_compactacao","deformacao_de_ruptura_no_ponto_de_compactacao","deformacao_fnal_no_ponto_de_compactacao","modulo_de_Young_secante_na_ruptura","deformacao_a_50_da_tensao_de_ruptura","modulo_de_Young_secante_a_50_da_tensao_de_ruptura","tensao_inicial_do_ensaio_edometrico_do_solo_mole","tensao_final_do_ensaio_edometrico_do_solo_mole","coeficiente_de_adensamento_do_solo_mole_ensaiado_no_edometro","principal_propriedade_do_solo_argiloso_determinada_no_ensaio_edometrico","coeficiente_de_adensamento_determinado_no_ensaio_esta_relacionado_com","nome_responsavel")
for experimento in experimentos.keys():
    url = base_url + experimentos[experimento]
    print experimento, url

    html = scraperwiki.scrape(url)
    gruposSoup = BeautifulSoup(html)
    grupos = gruposSoup.findAll( "div", {"class" : "defaulttemplate"} )
    lista = []
    num_grupo = 1
    for grupo in grupos:
        dados = {}
        dados['EXPERIMENTO'] = experimento
        linhas = grupo.findAll("tr")
        total_valores_grupo = len(linhas)
        for linha, categoria in zip(linhas, categorias):
            valores = []
            colunas = linha.findAll("td")
            if len(colunas) > 1:
                dados[categoria] = colunas[1].text
            else:
                dados['nome_responsavel'] = colunas[0].text
        dados['ID'] = num_grupo
        num_grupo += 1
        scraperwiki.sqlite.save(['ID'],dados)
                
        