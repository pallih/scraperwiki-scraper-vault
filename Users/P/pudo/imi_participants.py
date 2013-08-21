import scraperwiki

import requests
from lxml import html

URL = "http://www.imi.europa.eu/content/ongoing-projects"

res = requests.get(URL)
index = html.fromstring(res.content)

for link in index.findall('.//*[@class="research-project"]//h4/a'):
    d = {'acronym': link.text.strip('-').strip(), 
         'url': link.get('href')}

    res = requests.get(link.get('href'))
    detail = html.fromstring(res.content)

    subtitle = detail.find('.//*[@class="research-project"]//p').xpath('string()').strip()
    d['title'] = subtitle
    
    projects = detail.findall('.//*[@class="research-project"]')[2]
    for participant in projects.findall('.//li'):
        d['class'] = participant.getparent().getprevious().xpath('string()').strip()
        d['organisation'] = participant.text.strip()
        
        scraperwiki.sqlite.save(unique_keys=['organisation', 'acronym'], data=d)
        

