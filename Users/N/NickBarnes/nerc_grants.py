import scraperwiki
import BeautifulSoup
import re

from scraperwiki import datastore

limit = 10

grant_url_re = re.compile('list_full.asp\\?pcode=(.*)')

def scrape_all():
    all_url = 'http://gotw.nerc.ac.uk/thematic.asp'
    all_html = scraperwiki.scrape(all_url)
    all_soup = BeautifulSoup.BeautifulSoup(all_html)
    all_links = all_soup.findAll(href=re.compile('list_them.asp'))
    for link in all_links:
        scrape_program(link.string, 'http://gotw.nerc.ac.uk/'+link['href'])

def scrape_program(program_name, program_url):
    print "Scraping about %s from %s" % (program_name, program_url)
    program_html = scraperwiki.scrape(program_url)
    program_soup = BeautifulSoup.BeautifulSoup(program_html)
    grant_links = program_soup.findAll('a', attrs={'class': "awardtitle", 'href': grant_url_re})
    for link in grant_links:
        grant_code = grant_url_re.match(link['href']).group(1)
        grant_name = link.b.string
        scrape_grant(program_name, grant_name, 'http://gotw.nerc.ac.uk/'+link['href'])

def scrape_grant(program_name, grant_name, grant_url):
    print "Scraping about %s:'%s' from %s" % (program_name, grant_name, grant_url)
    grant_html = scraperwiki.scrape(grant_url)
    grant_soup = BeautifulSoup.BeautifulSoup(grant_html)
    print grant_soup
    # Now show that we can parse it
    global limit
    if limit == 0:
        return
    limit = limit-1
    abstract = grant_soup.find(text='Abstract:')
    print abstract.parent.parent
    value = grant_soup.find(text='Value:')
#    print value.parent.parent

scrape_all()

import scraperwiki
import BeautifulSoup
import re

from scraperwiki import datastore

limit = 10

grant_url_re = re.compile('list_full.asp\\?pcode=(.*)')

def scrape_all():
    all_url = 'http://gotw.nerc.ac.uk/thematic.asp'
    all_html = scraperwiki.scrape(all_url)
    all_soup = BeautifulSoup.BeautifulSoup(all_html)
    all_links = all_soup.findAll(href=re.compile('list_them.asp'))
    for link in all_links:
        scrape_program(link.string, 'http://gotw.nerc.ac.uk/'+link['href'])

def scrape_program(program_name, program_url):
    print "Scraping about %s from %s" % (program_name, program_url)
    program_html = scraperwiki.scrape(program_url)
    program_soup = BeautifulSoup.BeautifulSoup(program_html)
    grant_links = program_soup.findAll('a', attrs={'class': "awardtitle", 'href': grant_url_re})
    for link in grant_links:
        grant_code = grant_url_re.match(link['href']).group(1)
        grant_name = link.b.string
        scrape_grant(program_name, grant_name, 'http://gotw.nerc.ac.uk/'+link['href'])

def scrape_grant(program_name, grant_name, grant_url):
    print "Scraping about %s:'%s' from %s" % (program_name, grant_name, grant_url)
    grant_html = scraperwiki.scrape(grant_url)
    grant_soup = BeautifulSoup.BeautifulSoup(grant_html)
    print grant_soup
    # Now show that we can parse it
    global limit
    if limit == 0:
        return
    limit = limit-1
    abstract = grant_soup.find(text='Abstract:')
    print abstract.parent.parent
    value = grant_soup.find(text='Value:')
#    print value.parent.parent

scrape_all()

