# -*- coding: utf-8 -*-     

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://diraol.eng.br/dee/'
experimentos = {'R':"R.html"}#{'C':"C.html"}#{'P':"P.html"}
categorias = ("turma_areia_ensaiada","equipe","tipo_de_ensaio_de_resistencia_realizado","indice_de_vazios_max_da_areia_ensaiada","indice_de_vazios_min_da_areia_ensaiada","compacidade_relativa_CR_no_inicio_da_fase_de_cisalhamento_sob_a_primeira_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_primeira_tensao_normal","desloc_horizontal_final_residual_sob_a_primeira_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_primeira_tensao_normal","cR_no_inicio_da_fase_de_cisalhamento_sob_a_segunda_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_segunda_tensao_normal","desloc_horizontal_final_residual_sob_a_segunda_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_segunda_tensao_normal","cR_no_inicio_da_fase_de_cisalhamento_sob_a_terceira_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_terceira_tensao_normal","desloc_horizontal_final_residual_sob_a_terceira_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_terceira_tensao_normal","primeira_tensao_normal_do_ensaio","segunda_tensao_normal_do_ensaio","terceira_tensao_normal_do_ensaio","angulo_de_atrito_de_pico_da_areia_ensaiada","angulo_de_atrito_residual_da_areia_ensaiada","nome_responsavel")
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
                
        # -*- coding: utf-8 -*-     

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://diraol.eng.br/dee/'
experimentos = {'R':"R.html"}#{'C':"C.html"}#{'P':"P.html"}
categorias = ("turma_areia_ensaiada","equipe","tipo_de_ensaio_de_resistencia_realizado","indice_de_vazios_max_da_areia_ensaiada","indice_de_vazios_min_da_areia_ensaiada","compacidade_relativa_CR_no_inicio_da_fase_de_cisalhamento_sob_a_primeira_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_primeira_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_primeira_tensao_normal","desloc_horizontal_final_residual_sob_a_primeira_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_primeira_tensao_normal","cR_no_inicio_da_fase_de_cisalhamento_sob_a_segunda_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_segunda_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_segunda_tensao_normal","desloc_horizontal_final_residual_sob_a_segunda_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_segunda_tensao_normal","cR_no_inicio_da_fase_de_cisalhamento_sob_a_terceira_tensao_normal","cR_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","desloc_horizontal_na_tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","tensao_de_cisalhamento_max_pico_igual_ruptura_sob_a_terceira_tensao_normal","cR_na_tensao_de_cisalhamento_final_residual_sob_a_terceira_tensao_normal","desloc_horizontal_final_residual_sob_a_terceira_tensao_normal","tensao_de_cisalhamento_final_residual_sob_a_terceira_tensao_normal","primeira_tensao_normal_do_ensaio","segunda_tensao_normal_do_ensaio","terceira_tensao_normal_do_ensaio","angulo_de_atrito_de_pico_da_areia_ensaiada","angulo_de_atrito_residual_da_areia_ensaiada","nome_responsavel")
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
                
        