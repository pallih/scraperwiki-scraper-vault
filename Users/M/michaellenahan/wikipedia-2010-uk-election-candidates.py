import scraperwiki
import BeautifulSoup
from urllib2 import HTTPError

from scraperwiki import datastore

# NOTE: This has mainly been an exercise for me to learn scraperwiki and python.
# The work of getting candidates data in one place has already been done: 
# http://www.yournextmp.com 
# http://scraperwiki.com/scrapers/show/your-next-mp
# http://scraperwiki.com/scrapers/show/wikipedia-parliamentary-candidates
# http://scraperwiki.com/scrapers/show/wikipedia-list-of-constituencies

# TODO: Get constituencies from http://en.wikipedia.org/wiki/Constituencies_in_the_next_United_Kingdom_general_election #       Or from: http://www.theyworkforyou.com/boundaries/new-constituencies.tsv

constituencies = ['Putney', 'Wimbledon', 'Battersea']
for constituency in constituencies:
    try:
        html = scraperwiki.scrape('http://en.wikipedia.org/wiki/' + constituency + '_(UK_Parliament_constituency)')
        page = BeautifulSoup.BeautifulSoup(html)
    except HTTPError:
        continue

    # ASSUMPTIONS: a span, id=Election_results is contained within a h2. h2 is followed by the table of candidates.    
    # NOTE: This does not work for Battersea ... a better assumption would be to look for
    # <a href="/wiki/United_Kingdom_general_election,_2010" title="United Kingdom general election, 2010">
    
    # NOTE: It's a good idea to use wikipedia urls for Party and Constituency, rather than the text - more consistent.
    
    for span in page.findAll(id="Election_results"):
        h2 = span.parent
        # need to call nextSibling twice to get table
        table = h2.nextSibling.nextSibling
        for row in table.findAll('tr')[2:]:      
            if row.findAll('td')[0].a:
                party = row.findAll('td')[0].a.string
            candidate = row.findAll('td')[1].string
            if row.findAll('td')[1].a:
                candidate = row.findAll('td')[1].a.string
            if candidate:
                scraperwiki.sqlite.save(['constituency', 'party'],{'constituency':constituency, 'party':party, 'candidate':candidate})


import scraperwiki
import BeautifulSoup
from urllib2 import HTTPError

from scraperwiki import datastore

# NOTE: This has mainly been an exercise for me to learn scraperwiki and python.
# The work of getting candidates data in one place has already been done: 
# http://www.yournextmp.com 
# http://scraperwiki.com/scrapers/show/your-next-mp
# http://scraperwiki.com/scrapers/show/wikipedia-parliamentary-candidates
# http://scraperwiki.com/scrapers/show/wikipedia-list-of-constituencies

# TODO: Get constituencies from http://en.wikipedia.org/wiki/Constituencies_in_the_next_United_Kingdom_general_election #       Or from: http://www.theyworkforyou.com/boundaries/new-constituencies.tsv

constituencies = ['Putney', 'Wimbledon', 'Battersea']
for constituency in constituencies:
    try:
        html = scraperwiki.scrape('http://en.wikipedia.org/wiki/' + constituency + '_(UK_Parliament_constituency)')
        page = BeautifulSoup.BeautifulSoup(html)
    except HTTPError:
        continue

    # ASSUMPTIONS: a span, id=Election_results is contained within a h2. h2 is followed by the table of candidates.    
    # NOTE: This does not work for Battersea ... a better assumption would be to look for
    # <a href="/wiki/United_Kingdom_general_election,_2010" title="United Kingdom general election, 2010">
    
    # NOTE: It's a good idea to use wikipedia urls for Party and Constituency, rather than the text - more consistent.
    
    for span in page.findAll(id="Election_results"):
        h2 = span.parent
        # need to call nextSibling twice to get table
        table = h2.nextSibling.nextSibling
        for row in table.findAll('tr')[2:]:      
            if row.findAll('td')[0].a:
                party = row.findAll('td')[0].a.string
            candidate = row.findAll('td')[1].string
            if row.findAll('td')[1].a:
                candidate = row.findAll('td')[1].a.string
            if candidate:
                scraperwiki.sqlite.save(['constituency', 'party'],{'constituency':constituency, 'party':party, 'candidate':candidate})


