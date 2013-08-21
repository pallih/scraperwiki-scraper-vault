import scraperwiki

from bs4 import BeautifulSoup

import urllib

url = "http://www.funkhauseuropa.de/world_wide_music/playlists/index.phtml"

def get_playlist():

    # open url
    fh = urllib.urlopen(url)
    # read website
    html = fh.read()
    soup = BeautifulSoup(html)

    filter = "Die in der Sendung gespielten Titel".split()
    date = soup.select("#wsFhePlaylists")[0].find('input')['value']

    shows_table = soup.select(".wsSendeplanFhe")
    summary = []
    for table in shows_table:
        # extract name of the show from summary entry of table
        show_name = ' '.join([k for k in table['summary'].split() if k not in filter])
        shows_tr = table.select(".wsOdd") + table.select(".wsEven")
        
        # create dictionary entries containing songtitle, interpret, length..
        for tr in shows_tr:
            song = {}
            tds = tr.findAll(name='td')
            song['date'] = date
            song['time'] = tds[0].text
            song['id'] = date + '_' + song['time']
            song['interpret'] = tds[1].text
            song['title'] = tds[2].text
            if len(tds[3].text.split()) < 2:
                song['length'] = "Unknown"
            else: 
                song['length'] = tds[3].text  
            song['show'] = show_name
            summary.append(song)

    scraperwiki.sqlite.save(unique_keys=['id'], data=summary, table_name="playlist")
    

get_playlist()
