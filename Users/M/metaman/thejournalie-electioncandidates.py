import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def parse_candidate(url):
    c = {} #the candidate
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)


    # non optional properties
    c['name'] = soup.find('div', {'class' : 'post postMain'}).find('h1').text.split(": ")[1]
    c['image_url'] = soup.find('div', {'class' : 'img'}).img['src']
    c['party'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].div.text.split(':')[1]
    c['constituency'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].findAll('div')[1].text.split(':')[1]
    c['profile_text'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].p.text

    # optional attributes

    email = ""
    email_tag = soup.find('li', {'class' : 'email'})
    if email_tag:
        email = email_tag.a.text
    c['email'] = email

    website = ""
    website_tag = soup.find('li', {'class' : 'website'})
    if website_tag:
        website = website_tag.a['href']
    c['website'] = website

    phone = ""
    phone_tag = soup.find('li', {'class' : 'phone'})
    if phone_tag:
        phone = phone_tag.text
    c['phone'] = phone

    twitter = ""
    twitter_tag = soup.find('li', {'class' : 'twitter'})
    if twitter_tag:
        twitter = twitter_tag.a['href']
    c['twitter'] = twitter

    facebook = ""
    facebook_tag = soup.find('li', {'class' : 'facebook'})
    if facebook_tag:
        facebook = facebook_tag.a['href']
    c['facebook'] = facebook

    # policies, needs detection
    
    policy_indicator_tag = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[8].find('h5')
    if policy_indicator_tag and policy_indicator_tag.text == "Policies":
        policy_list = policy_indicator_tag = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[8].find('ul')
        policy_text = '; '.join(policy_list.findAll(text=True))
    else:
        policy_text = ""
    c['policy_text'] = policy_text

    return c


url1 = 'http://www.thejournal.ie/election-candidates-2011/dublin-central/john-hyland/'
url2 = 'http://www.thejournal.ie/election-candidates-2011/dublin-central/aine-clancy/'

url3 = 'http://www.thejournal.ie/election-candidates-2011/galway-east/tim-broderick'

candidate1 = parse_candidate(url3)

from pprint import pprint
pprint(candidate1)


import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def parse_candidate(url):
    c = {} #the candidate
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)


    # non optional properties
    c['name'] = soup.find('div', {'class' : 'post postMain'}).find('h1').text.split(": ")[1]
    c['image_url'] = soup.find('div', {'class' : 'img'}).img['src']
    c['party'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].div.text.split(':')[1]
    c['constituency'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].findAll('div')[1].text.split(':')[1]
    c['profile_text'] = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[3].p.text

    # optional attributes

    email = ""
    email_tag = soup.find('li', {'class' : 'email'})
    if email_tag:
        email = email_tag.a.text
    c['email'] = email

    website = ""
    website_tag = soup.find('li', {'class' : 'website'})
    if website_tag:
        website = website_tag.a['href']
    c['website'] = website

    phone = ""
    phone_tag = soup.find('li', {'class' : 'phone'})
    if phone_tag:
        phone = phone_tag.text
    c['phone'] = phone

    twitter = ""
    twitter_tag = soup.find('li', {'class' : 'twitter'})
    if twitter_tag:
        twitter = twitter_tag.a['href']
    c['twitter'] = twitter

    facebook = ""
    facebook_tag = soup.find('li', {'class' : 'facebook'})
    if facebook_tag:
        facebook = facebook_tag.a['href']
    c['facebook'] = facebook

    # policies, needs detection
    
    policy_indicator_tag = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[8].find('h5')
    if policy_indicator_tag and policy_indicator_tag.text == "Policies":
        policy_list = policy_indicator_tag = soup.find('div', {'class' : 'post postMain'}).find('div', {'class' : 'text'}).findAll('div')[8].find('ul')
        policy_text = '; '.join(policy_list.findAll(text=True))
    else:
        policy_text = ""
    c['policy_text'] = policy_text

    return c


url1 = 'http://www.thejournal.ie/election-candidates-2011/dublin-central/john-hyland/'
url2 = 'http://www.thejournal.ie/election-candidates-2011/dublin-central/aine-clancy/'

url3 = 'http://www.thejournal.ie/election-candidates-2011/galway-east/tim-broderick'

candidate1 = parse_candidate(url3)

from pprint import pprint
pprint(candidate1)


