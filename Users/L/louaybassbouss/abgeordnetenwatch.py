###############################################
# scraper for http://www.abgeordnetenwatch.de #
###############################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def scrap_members_of_parlament(url):
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html)
    mps = html.findAll('div', {'class': 'card'})
    for mp in mps:
        div = mp.find('div', {'class': 'abg_foto'})
        profile_url = 'http://www.abgeordnetenwatch.de/'+div.find('a')['href']
        photo_url = 'http://www.abgeordnetenwatch.de'+div.find('img')['src']
        div = mp.find(attrs = {'class': re.compile('basics.*')})
        divs = div.findAll('div')
        name = divs[0].text
        party = divs[1].text
        district = divs[2].text
        div = mp.find('div', {'class': 'infos'})
        questions = None
        answers = None
        match = re.match(r"(?P<questions>\d*) Fragen, (?P<answers>\d*) Antworten.*", div.text)
        if match != None:
            questions = match.group('questions')
            answers = match.group('answers')
        scraperwiki.sqlite.save(unique_keys=['url'], data={'url': profile_url, 'photo': photo_url, 'name': name, 'party': party, 'district': district, 'questions': questions, 'answers': answers})
    next_link_div = html.find('div',{'class':'browse next'})
    if next_link_div != None:
        next_link = next_link_div.find('a')
        if next_link != None:
            scrap_members_of_parlament('http://www.abgeordnetenwatch.de/'+next_link['href'].split('#')[0])

scrap_members_of_parlament('http://www.abgeordnetenwatch.de/abgeordnete-337-0.html')