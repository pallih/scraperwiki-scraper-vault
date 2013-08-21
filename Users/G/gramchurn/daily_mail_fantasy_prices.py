import scraperwiki

# Blank Python

import pycurl
import cStringIO
import lxml
from lxml import html
import pickle
import pprint 
import string
import csv
import HTMLParser
from lxml.html import fromstring, etree

team_names = { 'Arsenal': 'ARS', 'Aston Villa': 'AVL', 'Chelsea': 'CHE', 'Everton':'EVE', 'Fulham': 'FUL','Liverpool':'LIV','Manchester City': 'MCY', 'Manchester United':'MUN', 'Newcastle United':'NEW', 'Norwich City':'NOR','Queens Park Rangers':'QPR','Reading':'RDG','Southampton':'SOU','Stoke City':'STK','Sunderland':'SUN','Swansea City':'SWA','Tottenham Hotspur':'TOT','West Bromwich Albion':'WBA','West Ham United':'WHU','Wigan Athletic':'WIG'}
END_DATE = '12/12/2013'
h = HTMLParser.HTMLParser()
# function to get  a page from a link and get the links on that page
def get_data_from_link(url_link):
    buf = cStringIO.StringIO()
    d = pycurl.Curl()
    d.setopt(d.URL, url_link)
    d.setopt(d.WRITEFUNCTION, buf.write)
    d.perform()
    #pp = pprint.PrettyPrinter(indent=4)
    
    data = buf.getvalue()
    buf.close()
    d.close()
    return data


def get_prices(link):
    data = get_data_from_link(link)
    
    doc = fromstring(data)
    all_player_lists =doc.find_class('pla-list')
    players_string = ''
    records = []
    for i in range(0,4):
                for el in all_player_lists[i][0]:
                        player_info = dict(name = el.find_class('name')[0].text_content().replace(',',''),
                        team = el.find_class('team')[0].text_content(),
                        #last_pts = el.find_class('last_pts')[0].text_content(),
                        value = el.find_class('value')[0].text_content().replace(u'\u00A3','').replace('m',''),
                        )
                        records.append(player_info)

    scraperwiki.sqlite.save(['name'], records,table_name='prices')

get_prices('http://fantasyfootball.dailymail.co.uk/select-team/')