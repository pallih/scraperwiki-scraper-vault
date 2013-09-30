import scraperwiki
import urllib2
import BeautifulSoup

#Template scraper for extracting guest lists from amiando.com powered event websites. See https://scraperwiki.com/scrapers/eventbrite/

url_first = 'www.amiando.com/example' #the first page you see when you log in to go here
cookie = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookie)
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

outrows = ['firstname', 'lastname', 'job_title', 'facetime_yes_no', 'company', 'twitter', 'flickr', 'facebook', 'linkedin'] #you may edit this to match the fields in the target web site

def parser(page, mode):
    soup = BeautifulSoup.BeautifulSoup(page)
    if mode == 'ajax': #amiando doesn't return a new web page when you hit a link. rather it fires a psuedo ajax event that returns a chunk of javascript with html in xml cdata tags. What it returns depends on the contenst  in which the AJAX endpoint is called, so it's necessary to walk through the pages in order
    ns = ''
    for cd in soup.findAll(text=True):
        if isinstance(cd, BeautifulSoup.CData): #find the cdata blocks
            ns = ns + cd #concat them to derive the html page
            nsoup = BeautifulSoup.BeautifulSoup(ns) #feed them into the parser
        if mode == 'first': #the first page can be parsed in the normal way
            nsoup = soup
        divs = nsoup.findAll('div', {'class': 'userListItemCounterGuest clearfix'}) #get fields with data
        links = nsoup.findAll('a', {'onclick': True}) #get links for navigation
        for div in divs:
            d = {}
            guest_link = div.find('a')
            guest_info = [em.string for em in div.findAll('em', {'class': 'userDataItemContent'})]
            name = (guest_link.string).split(' ')
            firstname = name.pop(0)
            lastname = ' '.join(name)
            job_title = guest_info[0]
            if guest_info[1] in ('Yes', 'No'):
                facetime = guest_info[1]
                company = guest_info[2]
                d.update(firstname=firstname, lastname=lastname, job_title=job_title, facetime_yes_no=facetime, company=company)
            else:
                company = guest_info[1]
                d.update(firstname=firstname, lastname=lastname, job_title=job_title, company=company)
            for link in div.findAll('a', {'title': True}): #this handles fields that may or may not exist such as social network profiles. you may edit this as desired.
                if link['title'] == 'Twitter profile':
                    twitter = link['href']
                    d.update(twitter=twitter)
                if link['title'] == 'Flickr profile':
                    flickr = link['href']
                    d.update(flickr=flickr)
                if link['title'] == 'Facebook profile':
                    facebook = link['href']
                    d.update(facebook=facebook)
                if link['title'] == 'LinkedIn profile':
                    linkedin = link['href']
                    d.update(linkedin=linkedin)
                if link['title'] == 'Linkedin profile':
                    linkedin = link['href']
                    d.update(linkedin=linkedin)
            scraperwiki.sqlite.save(unique_keys=[firstname, lastname], data=d)

    if (links[-1]).string == '>>Next': #while we walk through the content, a "next" link will be avalable that always returns the next page (unlike the numbered page links, which are context dependent)
        nl = (links[-1]['onclick']).split('\'') #it's not a proper link of course (and scraperwiki syntax highlighting still doesn't like slash-escape) so we extract the actual URI from the javascript
        nextlink = 'http://www.amiando.com//' + str(nl[1]) #and make a real one 
    else:
        nextlink = 'stop' #no more nextlinks = job's a good'un.
    return nextlink

#start flow control - opens first page and begins while loop

page = urllib2.urlopen(url_first)
nextlink = parser(page, 'first')
while nextlink != 'stop':
  page = urllib2.urlopen(nextlink)
  nextlink = parser(page, 'ajax')
import scraperwiki
import urllib2
import BeautifulSoup

#Template scraper for extracting guest lists from amiando.com powered event websites. See https://scraperwiki.com/scrapers/eventbrite/

url_first = 'www.amiando.com/example' #the first page you see when you log in to go here
cookie = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookie)
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

outrows = ['firstname', 'lastname', 'job_title', 'facetime_yes_no', 'company', 'twitter', 'flickr', 'facebook', 'linkedin'] #you may edit this to match the fields in the target web site

def parser(page, mode):
    soup = BeautifulSoup.BeautifulSoup(page)
    if mode == 'ajax': #amiando doesn't return a new web page when you hit a link. rather it fires a psuedo ajax event that returns a chunk of javascript with html in xml cdata tags. What it returns depends on the contenst  in which the AJAX endpoint is called, so it's necessary to walk through the pages in order
    ns = ''
    for cd in soup.findAll(text=True):
        if isinstance(cd, BeautifulSoup.CData): #find the cdata blocks
            ns = ns + cd #concat them to derive the html page
            nsoup = BeautifulSoup.BeautifulSoup(ns) #feed them into the parser
        if mode == 'first': #the first page can be parsed in the normal way
            nsoup = soup
        divs = nsoup.findAll('div', {'class': 'userListItemCounterGuest clearfix'}) #get fields with data
        links = nsoup.findAll('a', {'onclick': True}) #get links for navigation
        for div in divs:
            d = {}
            guest_link = div.find('a')
            guest_info = [em.string for em in div.findAll('em', {'class': 'userDataItemContent'})]
            name = (guest_link.string).split(' ')
            firstname = name.pop(0)
            lastname = ' '.join(name)
            job_title = guest_info[0]
            if guest_info[1] in ('Yes', 'No'):
                facetime = guest_info[1]
                company = guest_info[2]
                d.update(firstname=firstname, lastname=lastname, job_title=job_title, facetime_yes_no=facetime, company=company)
            else:
                company = guest_info[1]
                d.update(firstname=firstname, lastname=lastname, job_title=job_title, company=company)
            for link in div.findAll('a', {'title': True}): #this handles fields that may or may not exist such as social network profiles. you may edit this as desired.
                if link['title'] == 'Twitter profile':
                    twitter = link['href']
                    d.update(twitter=twitter)
                if link['title'] == 'Flickr profile':
                    flickr = link['href']
                    d.update(flickr=flickr)
                if link['title'] == 'Facebook profile':
                    facebook = link['href']
                    d.update(facebook=facebook)
                if link['title'] == 'LinkedIn profile':
                    linkedin = link['href']
                    d.update(linkedin=linkedin)
                if link['title'] == 'Linkedin profile':
                    linkedin = link['href']
                    d.update(linkedin=linkedin)
            scraperwiki.sqlite.save(unique_keys=[firstname, lastname], data=d)

    if (links[-1]).string == '>>Next': #while we walk through the content, a "next" link will be avalable that always returns the next page (unlike the numbered page links, which are context dependent)
        nl = (links[-1]['onclick']).split('\'') #it's not a proper link of course (and scraperwiki syntax highlighting still doesn't like slash-escape) so we extract the actual URI from the javascript
        nextlink = 'http://www.amiando.com//' + str(nl[1]) #and make a real one 
    else:
        nextlink = 'stop' #no more nextlinks = job's a good'un.
    return nextlink

#start flow control - opens first page and begins while loop

page = urllib2.urlopen(url_first)
nextlink = parser(page, 'first')
while nextlink != 'stop':
  page = urllib2.urlopen(nextlink)
  nextlink = parser(page, 'ajax')
