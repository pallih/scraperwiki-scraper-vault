# My first ever scraperwiki scraper.  I've never used BeautifulSoup or
# scraperwiki before so please bear with me.
# 
# This is a really quick and dirty hack, because I woke up this morning
# and wanted to find out whether the BNP and UKIP had managed to retain
# any of their deposits in the 2010 general election, and I couldn't find
# the election results anywhere online.
#
# Nick Barnes, 2010-05-08

import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

def main():
    main_html = scraperwiki.scrape('http://news.bbc.co.uk/1/shared/election2010/results/')
    main_page = BeautifulSoup.BeautifulSoup(main_html)

    constituency_list = main_page.find('ol', attrs={'class': 'constituency-list'})
    # this is a big list of the constituencies.  If we just wanted
    # to know party results, we could get it from here.
    
    for constituency in constituency_list.findAll('li'): 
        seat = constituency.find('span', attrs={'class': 'seat'}).string
        # check whether seat previously fetched; this is an attempt to get around CPU time limit
        already = datastore.fetch({'seat': seat})
        if already and already[0]:
            if already[0]['data']['done'] == '1':
                print "Seat %s already in datastore" % seat
            else:
                print "Seat %s in datastore but not finished: %s" % (seat, already)
        else:
            print "Seat %s not in datastore; fetching..." % seat
            # I expect there's a better way to do this:
            link = 'http://news.bbc.co.uk' + constituency.find('a')['href']
            scrape_constituency(seat, link)
    
# Scrape the results from a single constituency page.    
def scrape_constituency(seat, url):    
    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)
    # there's all sorts of stuff on this page.  I couldn't find
    # a value for the total electorate, although it might be here.
    # There is a turnout line, with a percentage value, from which
    # one could back-compute the electorate.  I don't do that yet. 
    table = page.find('table', attrs={'class': 'candidate-detail'})
    for candidate_row in table.tbody.findAll('tr'):
        print candidate_row
        items = candidate_row.findAll('td')
        party_class = candidate_row['class']
        # unlike the rest of the scrape, here we do hard-coded indexes.
        name = items[0].span.string.strip()
        party = items[1].string.strip()
        votes_string = items[2].string.replace(',','')
        try:
            votes = int(votes_string)
        except:
            votes = None
        data = {'seat': seat, 'candidate': name, 'party': party, 'votes': votes}
        datastore.save(unique_keys=['seat', 'candidate', 'party'], data=data)
    datastore.save(unique_keys=['seat'],data={'seat':seat, 'done':True})
               
main()
