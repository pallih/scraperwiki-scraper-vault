import scraperwiki,re
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.bis.gov.uk'
starturl = 'http://www.bis.gov.uk/news/speeches?pp=50'

def strip_tags(value):
    "Return the given HTML with all tags stripped."
    return re.sub(r'<[^>]*?>', '', value)

def parse_speech(url):
    data = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    content = soup.find('div', {'id' : 'mainColumn' })
    title = content.h1.text
    author = content.find('p', {'class' : 'detail'}).text[2:]
    position = content.p.nextSibling.text
    date_and_place = content.find('p', {'class' : 'detail alternate'})
    date = date_and_place.text.partition(',')[0]
    place = date_and_place.text.partition(',')[2]
    body = content.findAll(lambda tag: len(tag.name) == 1 and not tag.attrs)

    # Re-join the body, otherwise it shows up with array cruft in the JSON
    body = ''.join(str(tag) for tag in body)

    data['title'] = title
    data['body'] = body
    data['minister_name'] = author
    data['minister_position'] = position
    data['date'] = date
    data['where'] = place
    data['source_url'] = url
    data['department'] = 'Business, Innovation and Skills'
    print "Save: " + str(data)
    scraperwiki.sqlite.save(["title", "source_url"], data)

def scrape_list(soup):
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(soup)
    soup.prettify()
    content = soup.find('ul', {'id' : 'listing' })
    items = content.findAll('li')
    for item in items:
        #title = item.h2.text
        url = 'http://www.bis.gov.uk' + item.h2.a['href']
        print 'Process: ' + url
        parse_speech(url)
        #minister = item.p.text[2:]
        #print minister
    #content_stuff = soup.findAll(text=True)
    #print content

def scrape_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_list(soup)
    next_link = soup.find("li", { "class" : "next" })
    #print next_link
    if next_link:
        next_url = base_url + next_link.a['href']
        #print next_url
        scrape_next_link(next_url)


scrape_next_link(starturl)
import scraperwiki,re
from BeautifulSoup import BeautifulSoup

base_url = 'http://www.bis.gov.uk'
starturl = 'http://www.bis.gov.uk/news/speeches?pp=50'

def strip_tags(value):
    "Return the given HTML with all tags stripped."
    return re.sub(r'<[^>]*?>', '', value)

def parse_speech(url):
    data = {}
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    soup.prettify()
    content = soup.find('div', {'id' : 'mainColumn' })
    title = content.h1.text
    author = content.find('p', {'class' : 'detail'}).text[2:]
    position = content.p.nextSibling.text
    date_and_place = content.find('p', {'class' : 'detail alternate'})
    date = date_and_place.text.partition(',')[0]
    place = date_and_place.text.partition(',')[2]
    body = content.findAll(lambda tag: len(tag.name) == 1 and not tag.attrs)

    # Re-join the body, otherwise it shows up with array cruft in the JSON
    body = ''.join(str(tag) for tag in body)

    data['title'] = title
    data['body'] = body
    data['minister_name'] = author
    data['minister_position'] = position
    data['date'] = date
    data['where'] = place
    data['source_url'] = url
    data['department'] = 'Business, Innovation and Skills'
    print "Save: " + str(data)
    scraperwiki.sqlite.save(["title", "source_url"], data)

def scrape_list(soup):
    #html = scraperwiki.scrape(url)
    #soup = BeautifulSoup(soup)
    soup.prettify()
    content = soup.find('ul', {'id' : 'listing' })
    items = content.findAll('li')
    for item in items:
        #title = item.h2.text
        url = 'http://www.bis.gov.uk' + item.h2.a['href']
        print 'Process: ' + url
        parse_speech(url)
        #minister = item.p.text[2:]
        #print minister
    #content_stuff = soup.findAll(text=True)
    #print content

def scrape_next_link(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    scrape_list(soup)
    next_link = soup.find("li", { "class" : "next" })
    #print next_link
    if next_link:
        next_url = base_url + next_link.a['href']
        #print next_url
        scrape_next_link(next_url)


scrape_next_link(starturl)
