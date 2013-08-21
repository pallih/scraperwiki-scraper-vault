# -*- coding: utf-8 -*-

import scraperwiki
from lxml.html import parse
import urllib
import datetime

# Blank Python

base_url = 'http://www.camara.gov.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp'
args = {'CampoOrdenacao': 'dtSessao',
  'PageSize': '1500',
  'TipoOrdenacao': 'DESC',
  'basePesq': 'plenario',
  'btnPesq': 'Pesquisar',
  'dtFim': '14%2F09%2F2011',
  'dtInicio': '14%2F09%2F2011',
  'txOrador': '',
  'txPartido': '',
  'txSumario': '',
  'txTexto': '',
  'txUF': ''}

def break_args(url):
    base_url, raw_args = url.split('?')
    args = {}
    for arg in raw_args.split('&'):
        query, value = arg.split('=')
        args[query] = value
    return args, base_url

def concatenate(args, base_url):
    c_args = base_url + '?'
    for arg in args:
        c_args = c_args + arg + "=" + args[arg] + '&'
    return c_args[:-1]

def scrapeSpeeches(html):
    table = html.cssselect('.tabela-1 tbody')
    rows = table[0].cssselect('tr')
    for row in rows:
        if row.get('style') == 'display: none':
            speech['text'] = row[0].text_content().strip()
            #print speech
            speech['id'] = makeId(speech['source_uri'])
            scraperwiki.sqlite.save(['id'], speech)
        else:
            speech = {}
            #according to the public statements schema 0.001
            #mandatory fields
            entity = row[5].text_content().split(',')
            speech['speaker_name'] = entity[0].strip()
            if len(entity)>1:
                speech['party'] = entity[1].strip() #was not in specs?
            else:
                speech['party'] = ''
            speech['text'] = ''#using summaries for now

            #optional fields
            speech['debate_id'] = row[1].text_content()
            speech['date'] = row[0].text_content()
            speech['start_time'] = row[6].text_content()
            #speech['speaker_id'] = 
            speech['venue_name'] = 'Plenário'
            #speech['venue_id'] 
            #speech['video_url'] 
            #speech['audio_url']
            #speech['speech_number']
            #speech['form_type'] = written (1), spoken (2)
            #speech['statement_type'] = vote explanation (1), emergency statement (2), procedural intervation, (3), campaign speech (4)
            #speech['version']
            speech['source_uri'] = 'http://www.camara.gov.br/internet/sitaqweb/' + row[3].cssselect('a')[0].get('href')

def getFullSpeech(url):
    html = parse(url).getroot()
    discurso = html.cssselect('div#content p[align="justify"] font[face="Arial"]')
    discurso = discurso[0].text_content().strip()
    return discurso

def saveDate(last_date):
    if last_date.year < 1900:
        end_date = datetime.datetime.today()
    last_date_string = datetime.datetime.strftime(last_date, '%d/%m/%Y')
    scraperwiki.sqlite.save_var('last_date', last_date_string)
    return last_date

def makeId(url):
    id_args, id_base = break_args(url)
    id = id_args['nuQuarto'] + '-' + id_args['nuOrador'] + '-' + id_args['nuInsercao'] + '-' + id_args['Data'] + '-' + id_args['dtHorarioQuarto']
    return id

last_date = scraperwiki.sqlite.get_var('last_date')
if last_date:
    end_date = datetime.datetime.strptime(last_date, '%d/%m/%Y')
else:
    end_date = datetime.datetime.today()

while True:
    start_date = end_date-datetime.timedelta(7)
    args['dtFim'] = str(end_date.day) + '%2F' + str(end_date.month) + '%2F' + str(end_date.year)
    args['dtInicio'] = str(start_date.day) + '%2F' + str(start_date.month) + '%2F' + str(start_date.year)
    url = concatenate(args, base_url)
    html = urllib.urlopen(url)
    html = parse(html).getroot()
    if html.cssselect('span.visualStrong'):
        print 'Scraping from ' + args['dtInicio'] + '-' + args['dtFim'] + ' for ' + html.cssselect('span.visualStrong')[3].text_content() + ' records'
        scrapeSpeeches(html)
    end_date = saveDate(start_date)