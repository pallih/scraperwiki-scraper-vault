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
import lxml.html
from lxml import etree
import json


'''Retrieve stations per id ('nucleo').

'''

sourcescraper = 'scrap_nucleos_cercanias'

scraperwiki.sqlite.attach('scrap_nucleos_cercanias')

nucleos = scraperwiki.sqlite.select(           
    '''* from scrap_nucleos_cercanias.swdata'''
)

'''Select train stations for each nucleo.

'''

stations_nucleos = {}

for nucleo in nucleos:

    stations = {}

    params = { "ciudad":nucleo['ciudad'], "nucleo":nucleo['id'] }
    
    html = scraperwiki.scrape("http://renfe.mobi/renfev2/hora_ga_cercanias.do", params)
    
    root = lxml.html.fromstring(html)
    
    etree_data = etree.fromstring(html)
    
    xpath_expression = etree.XPath("//select[@name='o']/option")
    
    options = xpath_expression(etree_data)
    
    for option in options:
    
        station = {}
        station['id'] = option.get('value')
        station['name'] = option.text
        station['nucleo_id'] = nucleo['id']
        stations[station['id'] ] = station

        # Save into DDBB
        scraperwiki.sqlite.save(unique_keys=['id', 'nucleo_id'], data=station)

    stations_nucleos[station['nucleo_id']] = stations

print json.dumps(stations_nucleos, sort_keys=True, indent=4)