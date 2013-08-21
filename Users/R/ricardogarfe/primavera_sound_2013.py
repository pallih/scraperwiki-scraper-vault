'''Copyright [2012] [Ricardo García Fernández]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import scraperwiki

import requests
import lxml.html
from lxml import etree

class PrimaveraSoundSchedule(object):
    def __init__(self):
        self.conciertos = {}
        api_url = 'http://www.primaverasound.es/programacion'
        config_req = requests.get(api_url)
        config_tree = lxml.html.fromstring(config_req.content)

        # Dias
        dls = config_tree.xpath('//*[@id="page-wrap"]/div[4]/div[2]/dl/dt')        
        # Conciertos
        dds = config_tree.xpath('//*[@id="page-wrap"]/div[4]/div[2]/dl/dd')
        
        self.dia = 20
        self.anyo = 2013
        self.mes = 05

        self.horarios = []
        self.parse_horarios(dls, dds)

    def parse_horarios(self, dls, dds):

        map(self.parse_horario_dia, dls, dds)

    def parse_horario_dia(self, dl, dd):
        
        ''' dl child
        <a href="#">Lunes 20 de mayo</a>
        '''
        dia = dl.find('a')
        dia = clean(text(dia))

        fecha = self.fecha_concierto()
        self.dia += 1

        ''' dd child table
        /div/table
        '''
        table_header = dd.find('div/table/thead/tr')
        columns_header = table_header.findall('th')

        conciertos = []
        table_contents = dd.findall('div/table/tbody/tr')
        for artist_data in table_contents:
            
            concierto = {}
            # Grupo
            artist_td_content = artist_data.find('td[1]')
            artist_content = artist_td_content.find('a')
            concierto[columns_header[0].text] = clean(text(artist_content))

            # Sala
            artist_sala = artist_data.find('td[2]')
            concierto[columns_header[1].text] = clean(text(artist_sala))

            # Hora
            artist_hora = artist_data.find('td[3]')
            concierto[columns_header[2].text] = clean(text(artist_hora))

            # id
            # <a href="artistaSingle?idArtista=143">Jupiter Lion</a>
            concierto_id = str(artist_content.attrib['href']).rsplit('=')[1:][0]
            concierto['id'] = concierto_id
            conciertos.append(concierto)

            # dia
            concierto['dia'] = fecha

            # Save to database
            scraperwiki.sqlite.save(unique_keys=['id'], data=concierto)

        self.horarios.append({'horario' : [dia, conciertos]})

    # Date for each concert in YYYY-MM-DD.
    def fecha_concierto(self):
        return str(self.anyo) + "-" + str(self.mes) + "-" + str(self.dia)

# Return element as text.
def text(element):
    return lxml.html.tostring(element, method='text', encoding=unicode)

# Trim whitespace and encode before uploading.
def clean(string):
    return string.strip().encode('utf-8')

primaveraSoundSchedule = PrimaveraSoundSchedule()

import pprint
pprint.pprint(primaveraSoundSchedule.horarios)

