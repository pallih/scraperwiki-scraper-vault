## These are libraries that we include that contain useful functions.
import scraperwiki
import requests
import lxml.html
import urllib
import csv

artist_csv = scraperwiki.scrape("https://docs.google.com/spreadsheet/pub?key=0ArqGpNBrUCUydHlCdXNWb3NoNW9TTmExVjZoSFRISFE&output=csv")
artists = csv.reader(artist_csv.splitlines())

# This is a function that returns the HTML for a given url.
def get_site(url):
    r = requests.get(url, verify=False)
    return lxml.html.fromstring(r.text)


def get_column(row, selector):
    try:
        return row.cssselect(selector)[0].text_content().strip()
    except:
        return ""

# This functions gets all the artist info and saves it to the database
def get_artist_info(artist):
    dom = get_site("http://www.allmusic.com/search/artists/" + artist)
    
    # Get all the elements on the page that have class .search-result
    result = dom.cssselect('.search-result')[0]
    link = result.cssselect('.name a')[0].get('href')
    
    
    types = ['main', 'compilations', 'singles']
    for music_type in types:
        print "Fetching all " + music_type
        dom = get_site(link + "/overview/" + music_type)
        
        
        # Get the album table
        table = dom.cssselect('.album-table')[0]
        
        # Get each row in the table
        rows = table.cssselect('tbody tr')
        
        # For every row, get the info we want.
        for row in rows:
            
            album = {
                "artist": artist,
                "year": get_column(row, '.year'),
                "title": get_column(row, '.title .full-title'),
                "label": get_column(row, '.label .full-title'),
                "type" : music_type
            }
            scraperwiki.sqlite.save(['artist','title','year','label'], album)

for artist in artists:
    print "Getting albums for " + artist[0]
    get_artist_info(artist[0])
        
        
