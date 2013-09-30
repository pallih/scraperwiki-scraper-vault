# Scrapes KW Realty associates' details

import scraperwiki
import lxml.html

# Records counter, used as ID in records
counter = 1

# Get root element
def scrape_content(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root

# Scrape cities
def parse_cities(root):
    div = root.cssselect('div.podsOfficeList')[1]
    #city = div.cssselect('ul a')[0].attrib['href']
    #print city
    for el in div.cssselect('ul a:first-child'):
        city = el.text_content()
        url = el.attrib['href']
        parse_associates(url)

# Get Associates' data from each city
def parse_associates (url):
    global counter
    root = scrape_content(url)
    for el in root.cssselect('div.agentPod'):
        res = dict()
        res['name'] = el.cssselect('b')[0].text_content()
        res['office'] = el.cssselect('span')[0].text_content()
        res['phone'] = el.cssselect('li.phone')[0].text_content()
        mail_data = el.cssselect('li.email a')[0].attrib['href']
        res['email'] = decipher_mail(mail_data)
        res['id'] = counter
        print scraperwiki.sqlite.save(unique_keys=['id'], data=res)
        counter += 1

def decipher_mail(data):
    data = data[15:].rstrip(')').split(',')
    return let(data[0].strip('"'), data[1], data[2])

def let(grandfather,alchemy,tree):
    grandfather += ' '
    length = len(grandfather)
    horse = 0
    drawer = ''
    index = 0
    while (index < length):
        horse = 0;
        while(ord(grandfather[index]) != 32):
            horse = horse * 10
            horse = horse + ord(grandfather[index]) - 48
            index = index + 1
        drawer += chr(shake(horse,int(alchemy),int(tree)))
        index = index + 1
    
#    if (arguments[3]):
#        drawer += arguments[3]
    
    return drawer


def shake(people,farm,historian):
    if (historian % 2 == 0):
        mathematical = 1;
        message = 1
        while (message <= historian / 2):
            memory = (people*people) % farm;
            mathematical = (memory*mathematical) % farm
            message = message + 1
    else:
        mathematical = people;
        member = 1
        while( member <= historian / 2):
            memory = (people*people) % farm;
            mathematical = (memory*mathematical) % farm;
            member = member + 1
    
    return mathematical

    

#src = 'http://www.kw.com/kw/OfficeSearchSubmit.action?stateProvId=TX'
src = 'http://kwallen.yourkwoffice.com/mcj/user/AssociateSearchSubmitAction.do?orgId=2021&rows=100'
#root = scrape_content(src)
#parse_cities(root)
parse_associates(src)

# Scrapes KW Realty associates' details

import scraperwiki
import lxml.html

# Records counter, used as ID in records
counter = 1

# Get root element
def scrape_content(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root

# Scrape cities
def parse_cities(root):
    div = root.cssselect('div.podsOfficeList')[1]
    #city = div.cssselect('ul a')[0].attrib['href']
    #print city
    for el in div.cssselect('ul a:first-child'):
        city = el.text_content()
        url = el.attrib['href']
        parse_associates(url)

# Get Associates' data from each city
def parse_associates (url):
    global counter
    root = scrape_content(url)
    for el in root.cssselect('div.agentPod'):
        res = dict()
        res['name'] = el.cssselect('b')[0].text_content()
        res['office'] = el.cssselect('span')[0].text_content()
        res['phone'] = el.cssselect('li.phone')[0].text_content()
        mail_data = el.cssselect('li.email a')[0].attrib['href']
        res['email'] = decipher_mail(mail_data)
        res['id'] = counter
        print scraperwiki.sqlite.save(unique_keys=['id'], data=res)
        counter += 1

def decipher_mail(data):
    data = data[15:].rstrip(')').split(',')
    return let(data[0].strip('"'), data[1], data[2])

def let(grandfather,alchemy,tree):
    grandfather += ' '
    length = len(grandfather)
    horse = 0
    drawer = ''
    index = 0
    while (index < length):
        horse = 0;
        while(ord(grandfather[index]) != 32):
            horse = horse * 10
            horse = horse + ord(grandfather[index]) - 48
            index = index + 1
        drawer += chr(shake(horse,int(alchemy),int(tree)))
        index = index + 1
    
#    if (arguments[3]):
#        drawer += arguments[3]
    
    return drawer


def shake(people,farm,historian):
    if (historian % 2 == 0):
        mathematical = 1;
        message = 1
        while (message <= historian / 2):
            memory = (people*people) % farm;
            mathematical = (memory*mathematical) % farm
            message = message + 1
    else:
        mathematical = people;
        member = 1
        while( member <= historian / 2):
            memory = (people*people) % farm;
            mathematical = (memory*mathematical) % farm;
            member = member + 1
    
    return mathematical

    

#src = 'http://www.kw.com/kw/OfficeSearchSubmit.action?stateProvId=TX'
src = 'http://kwallen.yourkwoffice.com/mcj/user/AssociateSearchSubmitAction.do?orgId=2021&rows=100'
#root = scrape_content(src)
#parse_cities(root)
parse_associates(src)

