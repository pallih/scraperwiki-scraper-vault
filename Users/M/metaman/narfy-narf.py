import scraperwiki
import time
import random

url = 'http://www.thejournal.ie/election-candidates-2011/'

from BeautifulSoup import BeautifulSoup

def getDetails(url):
    c = {} #the candidate
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    

    # non optional properties
    c['url'] = url
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

    scraperwiki.datastore.save(['constituency','name'], c)

def scrapeCons():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  cons = soup.find('div',{'class':'river span-8'}).find('div',{'class':'post'}).findAll('h3')
  urls = []
  for con in cons:
    urls.append({'href':con.find('a')['href'],'text':con.find('a').text})
  return urls

def scrapeCandidate(key,txt):
  u = url + key
  html = scraperwiki.scrape(u)
  soup = BeautifulSoup(html)
  divs = soup.find('div',{'id':'sort_holder'}).findAll('div',{'class':'post postDiscussed-candidate span-4'})
  for div in divs:
    a = div.find('div',{'class':'text'}).find('a')
    getDetails(a['href'] + '/')
    
  
urls = scrapeCons()
for u in urls:
  scrapeCandidate(u['href'][2:]+'/',u['text'])
  time.sleep(random.uniform(1, 4) )


import scraperwiki
import time
import random

url = 'http://www.thejournal.ie/election-candidates-2011/'

from BeautifulSoup import BeautifulSoup

def getDetails(url):
    c = {} #the candidate
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)

    

    # non optional properties
    c['url'] = url
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

    scraperwiki.datastore.save(['constituency','name'], c)

def scrapeCons():
  html = scraperwiki.scrape(url)
  soup = BeautifulSoup(html)
  cons = soup.find('div',{'class':'river span-8'}).find('div',{'class':'post'}).findAll('h3')
  urls = []
  for con in cons:
    urls.append({'href':con.find('a')['href'],'text':con.find('a').text})
  return urls

def scrapeCandidate(key,txt):
  u = url + key
  html = scraperwiki.scrape(u)
  soup = BeautifulSoup(html)
  divs = soup.find('div',{'id':'sort_holder'}).findAll('div',{'class':'post postDiscussed-candidate span-4'})
  for div in divs:
    a = div.find('div',{'class':'text'}).find('a')
    getDetails(a['href'] + '/')
    
  
urls = scrapeCons()
for u in urls:
  scrapeCandidate(u['href'][2:]+'/',u['text'])
  time.sleep(random.uniform(1, 4) )


