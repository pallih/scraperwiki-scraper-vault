import scraperwiki

# Blank Python

URL = "http://www.imi.europa.eu/content/ongoing-projects"

import requests
response = requests.get(URL)

from lxml import html 
document = html.fromstring(response.content)


headers = document.findall('.//*[@class="list-subtitle"]/h4')

for header in headers:
    url = header.find('a').get('href')
    response = requests.get(url)    
    details = html.fromstring(response.content)
    print details.find('.//h3').text_content()
    partners = details.findall('.//*[@class="research-project"]//li')
    for partner in partners:
        print partner.text_content()

        data = {'project': details.find('.//h3').text_content(), 
                'partner': partner.text_content()}
        scraperwiki.sqlite.save(unique_keys=['project', 'partner'], data=data)