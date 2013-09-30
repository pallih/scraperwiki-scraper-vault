# -*- coding: utf-8 -*-     

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://diraol.eng.br/dee/'
experimentos = {'P':"P.html"}#{'C':"C.html"}#{'R':"R.html"}
categorias = ('turma_areia_ensaiada','equipe','permeametro_utilizado','altura_meda_do_cp','perda_de_carga_na_metade_superior_do_cp','perda_de_carga_na_metade_inferior_do_cp','gradiente_hidraulico_na_metade_superior_do_cp','gradiente_hidraulico_na_metade_inferior_do_cp','area_da_secao_transversall_do_cp','vazao_medida','condutividade_hidraulica_na_metade_superior','condutividade_hidraulica_na_metade_inferior','indice_de_vazios_maximo_da_areia_ensaiada','indice_de_vazios_minimo_da_areia_ensaiada','indice_de_vazios_medio_do_cp_ensaiado','compacidade_relativa_CR_media_do_cp_ensaiado','estimativa_do_indice_de_vazios_da_metade_superior_do_cp','estimativa_do_indice_de_vazios_da_metade_inferior_do_cp','estimativa_da_CR_da_metade_superior_do_cp','estimativa_da_CR_da_metade_inferior_do_cp','fracao_argila_da_areia_ensaiada','fracao_silte_da_areia_ensaiada','fracao_areia_da_areia_ensaiada','fracao_pedregulho_da_areia_ensaiada','coeficiente_de_nao_uniformidade_CNU_da_areia_ensaiada','d15_da_areia_ensaiada','fracao_argila_do_solo_A','fracao_silte_do_solo_A','fracao_areia_do_solo_A','fracao_pedregulho_do_solo_A','cNU_do_solo_A','d15_do_solo_A','d85_do_solo_A','areia_ensaiada_serve_de_filtro-dreno_para_solo_A','limite_de_liquidez_do_solo_argiloso_ensaiado','limite_de_plasticidade_do_solo_argiloso_ensaiado','indice_de_plasticidade_do_solo_argiloso_ensaiado', 'nome_responsavel')
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
experimentos = {'P':"P.html"}#{'C':"C.html"}#{'R':"R.html"}
categorias = ('turma_areia_ensaiada','equipe','permeametro_utilizado','altura_meda_do_cp','perda_de_carga_na_metade_superior_do_cp','perda_de_carga_na_metade_inferior_do_cp','gradiente_hidraulico_na_metade_superior_do_cp','gradiente_hidraulico_na_metade_inferior_do_cp','area_da_secao_transversall_do_cp','vazao_medida','condutividade_hidraulica_na_metade_superior','condutividade_hidraulica_na_metade_inferior','indice_de_vazios_maximo_da_areia_ensaiada','indice_de_vazios_minimo_da_areia_ensaiada','indice_de_vazios_medio_do_cp_ensaiado','compacidade_relativa_CR_media_do_cp_ensaiado','estimativa_do_indice_de_vazios_da_metade_superior_do_cp','estimativa_do_indice_de_vazios_da_metade_inferior_do_cp','estimativa_da_CR_da_metade_superior_do_cp','estimativa_da_CR_da_metade_inferior_do_cp','fracao_argila_da_areia_ensaiada','fracao_silte_da_areia_ensaiada','fracao_areia_da_areia_ensaiada','fracao_pedregulho_da_areia_ensaiada','coeficiente_de_nao_uniformidade_CNU_da_areia_ensaiada','d15_da_areia_ensaiada','fracao_argila_do_solo_A','fracao_silte_do_solo_A','fracao_areia_do_solo_A','fracao_pedregulho_do_solo_A','cNU_do_solo_A','d15_do_solo_A','d85_do_solo_A','areia_ensaiada_serve_de_filtro-dreno_para_solo_A','limite_de_liquidez_do_solo_argiloso_ensaiado','limite_de_plasticidade_do_solo_argiloso_ensaiado','indice_de_plasticidade_do_solo_argiloso_ensaiado', 'nome_responsavel')
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
                
        