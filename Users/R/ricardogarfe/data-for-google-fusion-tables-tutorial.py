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

html = scraperwiki.scrape("http://delgado.tv/google-fusion/")
root = lxml.html.fromstring(html)

class Link(object):
     def __init__(self, name, href):
         self.name = name
         self.href = href

data_links = {}

id = 0

data_links_found = root.cssselect("a")

for data_link in data_links_found:

    id += 1

    link = {}

    link['name'] = data_link.text

    link['href'] = data_link.attrib['href']
    
    link['id'] = id;
    
    data_links[link['id']] = link
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=link)

print json.dumps(data_links, sort_keys=True, indent=4)
    

