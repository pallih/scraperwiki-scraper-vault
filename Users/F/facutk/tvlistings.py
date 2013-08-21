import scraperwiki

# Blank Python

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from cgi import parse_qs
from urlparse import urlparse


def get_lineup_id( href ):
    """docstring for get_ch_number"""
    return parse_qs( urlparse( href ).query )['lineupId'][0]

def get_zipcode_lineups( zipcode ):
    lineups = []
    """docstring for def process_zipcode"""
    #print 'zipcode: ', zipcode
    baseurl = 'http://tvlistings.zap2it.com'
    url = baseurl + '/tvlistings/ZBChooseProvider.do?method=getProviders'

    # Prepare the data
    values = {'zipcode' : zipcode}
    data = urllib.urlencode(values)
     
    # Send HTTP POST request
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
     
    html = response.read()
     
    # Print the result
    # print html
    lineup = None
    soup = BeautifulSoup(html)
    result = soup.findAll('div', {'class': 'zc-provider-list'})
    for div in result:
        links = div.findAll('a')
        for a in links:
            channel_name = a.contents[0].strip().replace('&amp;','&')

            lineupid = get_lineup_id( a['href'] )


            lineup = { 'zipcode': zipcode,
                       'lineup':lineupid,
                       'description':channel_name
                     }
    if lineup:
        scraperwiki.sqlite.save( unique_keys=[ 'zipcode', 'lineup', 'description' ], data=lineup )

for k in range(90000,95000):
    get_zipcode_lineups( k )