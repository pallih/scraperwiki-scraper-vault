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
import json

'''Retrieve cities with 'nucleo'

'''

html = scraperwiki.scrape("http://renfe.mobi/renfev2/ciudades_cercanias.do")
root = lxml.html.fromstring(html)

class Nucleo(object):
     def __init__(self, name):
         self.name = name

nucleos = {}

for nucleo_link in root.cssselect("p a"):

    nucleo = {}

    attribute_list = str(nucleo_link.attrib['href']).rsplit('&')[1:]

    if attribute_list:
    
        nucleo['name'] = nucleo_link.text
    
        nucleo['ciudad'] = attribute_list[0].rsplit('=')[1:][0]
        
        nucleo['id'] = attribute_list[1].rsplit('=')[1:][0]
        
        nucleos[nucleo['id']] = nucleo
        
        scraperwiki.sqlite.save(unique_keys=['id'], data=nucleo)

print json.dumps(nucleos, sort_keys=True, indent=4)
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
import json

'''Retrieve cities with 'nucleo'

'''

html = scraperwiki.scrape("http://renfe.mobi/renfev2/ciudades_cercanias.do")
root = lxml.html.fromstring(html)

class Nucleo(object):
     def __init__(self, name):
         self.name = name

nucleos = {}

for nucleo_link in root.cssselect("p a"):

    nucleo = {}

    attribute_list = str(nucleo_link.attrib['href']).rsplit('&')[1:]

    if attribute_list:
    
        nucleo['name'] = nucleo_link.text
    
        nucleo['ciudad'] = attribute_list[0].rsplit('=')[1:][0]
        
        nucleo['id'] = attribute_list[1].rsplit('=')[1:][0]
        
        nucleos[nucleo['id']] = nucleo
        
        scraperwiki.sqlite.save(unique_keys=['id'], data=nucleo)

print json.dumps(nucleos, sort_keys=True, indent=4)
    