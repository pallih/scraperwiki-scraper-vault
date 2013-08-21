### TO DO: 
### Find dates for press releases
### Convert dates, once found: json friendly
### Convert phone numbers: 000-000-0000
import re
import requests
import lxml.html
from pyquery import PyQuery as pq
import scraperwiki

BASE_URL = 'http://perlmutter.house.gov/'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("7d660b22024443558b551da3d39145cd", "P000593")

def scrape_bio():

    url = BASE_URL + 'index.php?option=com_content&view=article&id=3&Itemid=4'

    request = requests.get(url, timeout=60)
    html = request.content
    
    container = pq(html)('div.article-content')
    content = pq(container).text()
    
    gasp.add_biography(content, url=url)

def scrape_socialmedia():
    
    request = requests.get(BASE_URL, timeout=60)
    html = request.content
    
    elems = pq(html)("div#boxs_2nd_content table td a")[-4:]
    
    gasp.add_facebook(elems[0].attrib['href'])
    gasp.add_twitter(elems[1].attrib['href'])
    gasp.add_social_media('rss', BASE_URL + elems[2].attrib['href'])
    gasp.add_youtube(elems[3].attrib['href'])

def scrape_issues():
    
    url = BASE_URL + 'index.php?option=com_content&view=article&id=676&Itemid=32'
    
    request = requests.get(url, timeout=60)
    html = request.content
    
    elems = pq(html)("ul.menu li a")
    
    for value in elems[:10]:
        url = value.attrib['href']
        
        request = requests.get(url, timeout=60)
        html = request.content

        title = pq(html)('h2.contentheading')
        title = pq(title).text()
        
        container = pq(html)('div.article-content p')[:4]
        content = pq(container).text()
        
        gasp.add_issue(title, content.strip(), url=url)

def scrape_offices():
    
    request = requests.get(BASE_URL, timeout=60)
    html = request.content

    container = pq(html)('div#footer div.moduletable table')
    for elem in pq(container)('td')[:2]:

        office = pq(elem)('strong').text()
        
        content = pq(elem).text().replace('.', '')
        
        address_re = re.compile(r'(.*)\s+Phone:\s+([\d\D\s]+)\sFax:\s+([\d\D\s]+)')
        
        (address, phone, fax) = address_re.match(content).groups()
        
        gasp.add_office(address, phone, fax=fax)
        
def scrape_pressreleases():
    
    url = BASE_URL + 'index.php?option=com_content&view=category&id=33&Itemid=15'
    
    request = requests.get(url, timeout=60)
    html = request.content
    
    for elem in pq(html)('div#mainbodyContentleft table a')[2:]:
        
        url = BASE_URL + elem.attrib['href']
        request = requests.get(url, timeout=60)
        html = request.content
        
        title = pq(html)("h2.contentheading").text()

        if not title:
            title = pq(html)("h3").text()
       
        container = pq(html)('div.article-content')
        content = pq(container).text()
        date = 'Not available'

        gasp.add_press_release(title, date, content, url=url)

    
scrape_bio()
scrape_socialmedia()
scrape_issues()
scrape_offices()
scrape_pressreleases()

gasp.finish()