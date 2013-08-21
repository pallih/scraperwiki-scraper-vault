# Scraping SALICWEB

import scraperwiki
import urllib
import BeautifulSoup


base_url = 'http://sistemas.cultura.gov.br/salicnet/conSituacao/conSituacao.php'
base_args = '?nmgp_opcao=busca&situacao_cond=df&situacao=Projeto+Cancelado%23%23%40%40Projeto+Cancelado&p_dtsituacao_cond=eq&p_dtsituacao_dia=&p_dtsituacao_mes=&p_dtsituacao_ano=&p_dtsituacao_input_2_dia=&p_dtsituacao_input_2_mes=&p_dtsituacao_input_2_ano=&p_mecanismo_cond=eq&p_mecanismo=&area_cond=eq&area=&o_sigla_cond=eq&o_sigla=&modalidade_cond=eq&modalidade=&escolher_cond=eq&escolher=nrprojeto%40%3F%40p_nomeprojeto%40%3F%40situacao%40%3F%40p_dtsituacao%40%3F%40area%40%3F%40o_sigla%40%3F%40modalidade%40%3F%40solicitado%40%3F%40aprovado%40%3F%40captado&ordenar_cond=eq&ordenar_ordem=on&ordenar=%2Bp.DtSituacao&NM_operador=and&nmgp_tab_label=situacao%3F%23%3FSitua%E7%E3o%3F%40%3Fp_dtsituacao%3F%23%3FDt.Situa%E7%E3o%3F%40%3Fp_mecanismo%3F%23%3FMecanismo%3F%40%3Farea%3F%23%3F%C1rea+Cultural%3F%40%3Fo_sigla%3F%23%3F%D3rg%E3o%3F%40%3Fmodalidade%3F%23%3FModalidade%3F%40%3Fescolher%3F%23%3FEscolher+campos%3F%40%3Fordenar%3F%23%3FOrdenar+campos%3F%40%3F&bprocessa=pesq&NM_filters=&nmgp_save_option=&nmgp_save_name=&NM_filters_del=&form_condicao=3'

start_arg = '&script_case_init='

def getProjects(start_project=1):
    html = urllib.urlopen(base_url + base_args + start_arg + str(start_project))
    soup = BeautifulSoup.BeautifulSoup(html)
    print soup

getProjects(1)