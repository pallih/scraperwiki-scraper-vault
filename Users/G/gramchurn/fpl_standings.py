import scraperwiki

import pycurl
import cStringIO
import lxml
from lxml import html
import pickle
import pprint 
import string
from lxml.html import fromstring

# function to get  a page from a link and get the links on that page
def get_rankings(url_link):
    buf = cStringIO.StringIO()
    d = pycurl.Curl()
    d.setopt(d.URL, url_link)
    d.setopt(d.WRITEFUNCTION, buf.write)
    d.perform()

    #pp = pprint.PrettyPrinter(indent=4)
    
    data = buf.getvalue()
    buf.close()
    d.close()
    doc = fromstring(data)
    table_standings = doc.find_class('ismStandingsTable')[0]
    count = 1
    prev_rank = 0
    for row in table_standings[2:]:
        curr_rank = int(row[1].text.replace(',',''))
       
        if curr_rank == prev_rank:
            count +=1
        else:
            rank = {
                'rank_no' : curr_rank,
                'no_people' : count,
                'overall_score' : row[5].text,
            }
            count =1
            prev_rank = int(curr_rank)
            scraperwiki.sqlite.save(['overall_score','rank_no'], rank, table_name='standings')
        
    
def main():

    link = 'http://fantasy.premierleague.com/my-leagues/303/standings/?ls-page='

    for num in range(1,3000):
        get_rankings(link+str(num))

main()
import scraperwiki

import pycurl
import cStringIO
import lxml
from lxml import html
import pickle
import pprint 
import string
from lxml.html import fromstring

# function to get  a page from a link and get the links on that page
def get_rankings(url_link):
    buf = cStringIO.StringIO()
    d = pycurl.Curl()
    d.setopt(d.URL, url_link)
    d.setopt(d.WRITEFUNCTION, buf.write)
    d.perform()

    #pp = pprint.PrettyPrinter(indent=4)
    
    data = buf.getvalue()
    buf.close()
    d.close()
    doc = fromstring(data)
    table_standings = doc.find_class('ismStandingsTable')[0]
    count = 1
    prev_rank = 0
    for row in table_standings[2:]:
        curr_rank = int(row[1].text.replace(',',''))
       
        if curr_rank == prev_rank:
            count +=1
        else:
            rank = {
                'rank_no' : curr_rank,
                'no_people' : count,
                'overall_score' : row[5].text,
            }
            count =1
            prev_rank = int(curr_rank)
            scraperwiki.sqlite.save(['overall_score','rank_no'], rank, table_name='standings')
        
    
def main():

    link = 'http://fantasy.premierleague.com/my-leagues/303/standings/?ls-page='

    for num in range(1,3000):
        get_rankings(link+str(num))

main()
