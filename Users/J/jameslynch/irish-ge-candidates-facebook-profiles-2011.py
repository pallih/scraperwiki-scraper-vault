import scraperwiki
import re

from BeautifulSoup import BeautifulSoup

def scrapeFacebookProfiles(pageLink):
    html = scraperwiki.scrape(pageLink)
    soup = BeautifulSoup(html)
    conName = soup.html.head.title
    links = soup.findAll(title=re.compile("Facebook$"))
    for link in links:
        words = link['title'].split(' on Facebook')
        print words[0] + "," + link.text + "," + link['href'] + "," + conName.text
        party = ""
        try :
            partyel = link.parent.previousSibling.previousSibling.previousSibling.previousSibling
            party = partyel.text
        except:
            try:
                partyel = link.parent.parent.previousSibling.previousSibling.previousSibling.previousSibling
                party = partyel.text
            except:
                break
        record = {}
        record['name'] = words[0]
        record['party'] = party
        record['fb_link'] = link['href']
        fans = link.text.split(' ')
        record['fb_fans'] = fans[0]
        record['constituency'] = conName.text
        scraperwiki.datastore.save(["name"], record)


def scrapePageLinks(homepage):
    homepageHTML = scraperwiki.scrape(homepage)
    hpSoup = BeautifulSoup(homepageHTML)
    cons = hpSoup.findAll(attrs={'class' : re.compile("fadeThis ")})
    for con in cons:
        scrapeFacebookProfiles(con['href'])

scrapePageLinks('http://www.candidate.ie')import scraperwiki
import re

from BeautifulSoup import BeautifulSoup

def scrapeFacebookProfiles(pageLink):
    html = scraperwiki.scrape(pageLink)
    soup = BeautifulSoup(html)
    conName = soup.html.head.title
    links = soup.findAll(title=re.compile("Facebook$"))
    for link in links:
        words = link['title'].split(' on Facebook')
        print words[0] + "," + link.text + "," + link['href'] + "," + conName.text
        party = ""
        try :
            partyel = link.parent.previousSibling.previousSibling.previousSibling.previousSibling
            party = partyel.text
        except:
            try:
                partyel = link.parent.parent.previousSibling.previousSibling.previousSibling.previousSibling
                party = partyel.text
            except:
                break
        record = {}
        record['name'] = words[0]
        record['party'] = party
        record['fb_link'] = link['href']
        fans = link.text.split(' ')
        record['fb_fans'] = fans[0]
        record['constituency'] = conName.text
        scraperwiki.datastore.save(["name"], record)


def scrapePageLinks(homepage):
    homepageHTML = scraperwiki.scrape(homepage)
    hpSoup = BeautifulSoup(homepageHTML)
    cons = hpSoup.findAll(attrs={'class' : re.compile("fadeThis ")})
    for con in cons:
        scrapeFacebookProfiles(con['href'])

scrapePageLinks('http://www.candidate.ie')