import re
import requests
from pyquery import PyQuery as pq
import scraperwiki

BASE_URL = 'http://akin.house.gov/'

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("7d660b22024443558b551da3d39145cd", "A000358")

def scrape_bio():

    url = BASE_URL + 'index.php?option=com_content&view=article&id=9&Itemid=2'

    request = requests.get(url, timeout=60)
    html = request.content
    
    container = pq(html)('.contentpaneopen p')
    content = pq(container).text()
    
    gasp.add_biography(content, url=url)

def scrape_socialmedia():
    
    request = requests.get(BASE_URL, timeout=60)
    html = request.content
    
    links = pq(html)("#footer-links a")
    
    gasp.add_social_media('rss', BASE_URL + links[0].attrib['href'])
    gasp.add_youtube(links[1].attrib['href'])
    gasp.add_facebook(links[2].attrib['href'])
    gasp.add_twitter(links[3].attrib['href'])

scrape_bio()
scrape_socialmedia()
gasp.finish()