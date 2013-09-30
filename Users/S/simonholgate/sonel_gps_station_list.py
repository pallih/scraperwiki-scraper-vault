import scraperwiki
import scrapemark
import urllib
import sys
import time
import re

def get_list():
    #read = True
    #while read:
        url = 'http://www.sonel.org/-GPS,28-.html?lang=en' 
        html = urllib.urlopen(url).read()
        #print html
        data = scrapemark.scrape("""
        {*
                        <div><span>[stations].id</span><div></div></div><div><b>GPS : </b>{{ [stations].name }}<br /><b>Latitude : </b>{{ [stations].lat }}<br /><b>Longitude : </b>{{ [stations].lon }}<br /><b>Fournisseur : </b>GSI<br /><a href="{{ [stations].href }}">Informations de la station</a><br /></div>
        *}
        """, html=html)
        rows = []
        for dataset in data['stations']:
            #print dataset
            rows.append(dataset)
        # save data
        scraperwiki.sqlite.save(['id'], rows, table_name="sonel_gps_station_list")

get_list()import scraperwiki
import scrapemark
import urllib
import sys
import time
import re

def get_list():
    #read = True
    #while read:
        url = 'http://www.sonel.org/-GPS,28-.html?lang=en' 
        html = urllib.urlopen(url).read()
        #print html
        data = scrapemark.scrape("""
        {*
                        <div><span>[stations].id</span><div></div></div><div><b>GPS : </b>{{ [stations].name }}<br /><b>Latitude : </b>{{ [stations].lat }}<br /><b>Longitude : </b>{{ [stations].lon }}<br /><b>Fournisseur : </b>GSI<br /><a href="{{ [stations].href }}">Informations de la station</a><br /></div>
        *}
        """, html=html)
        rows = []
        for dataset in data['stations']:
            #print dataset
            rows.append(dataset)
        # save data
        scraperwiki.sqlite.save(['id'], rows, table_name="sonel_gps_station_list")

get_list()