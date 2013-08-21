# Blank Python

import sys

from scraperwiki import scrape as GET, sqlite as datastore
from scrapemark import scrape
from lxml.html import fromstring, tostring
from lxml.html.clean import clean_html
import cookielib

cookie_jar = cookielib.CookieJar()

URL = "http://www.artcyclopedia.com/"

MOVEMENTS_INDEX = """<table>
<b>Art Movements</b>

{* <a href="{{ [movements].link }}">{{ [movements].title }}</a> *}

</table>"""

MOVEMENTS_INDIVIDUAL = """<div id="mainpage">

<h2></h2>
{* <a href="{{ [related].link }}">{{ [related].topic }}</a> *}


<center>
<b>Chronological</b>

{* <td><a href="{{ [artists].profile_link|abs }}">{{ [artists].name }}</a></td><td>{{ [artists].alive }}</td><td>{{ [artists].artist_type }}</td><td><img src="{{ [artists].thumbnail_link|abs }}"></img></td> *}
</center>

</div>
"""

MOVEMENTS_INDIVIDUAL2 = """<div id="mainpage">

<center>
<h2></h2>
{* <a href="{{ [related].link }}">{{ [related].topic }}</a> *}
</center>


{* <td>{{ [artists].name }}</td><td>{{ [artists].alive }}</td><td>{{ [artists].artist_type }}</td><td><img src="{{ [artists].thumbnail_link|abs }}"></img></td> *}


</div>
"""


def get_page(url):
    return tostring(fromstring(GET(url)))

#print scrape(MOVEMENTS_INDIVIDUAL2, html=get_page("http://www.artcyclopedia.com/history/american-scene.html"))
#print scrape(MOVEMENTS_INDEX, html=get_page(URL))

def main():
    movements = scrape(MOVEMENTS_INDEX, html=get_page(URL))
    print movements
    for m in movements['movements']:
        if 'artcyclopedia.com' in m['link']:
            movement = scrape(MOVEMENTS_INDIVIDUAL, html=get_page(m['link']))
            print m['title']
            if not movement:
                movement = scrape(MOVEMENTS_INDIVIDUAL2, html=get_page(m['link']))

            relations = []
            for relation in movement['related']:
                r = dict(movement=m['title'], related_to=relation['topic'])
                if '/artists/' in relation['link']:
                    r['topic'] = 'artist'
                else:
                    r['topic'] = 'movement'
                relations.append(r)
    
            artists = []
            for artist in movement['artists']:
                artist['movement'] = m['title']
                dates = artist['alive'].split('-')
                try:
                    artist['birth_year'] = int(dates[0])
                    artist['death_year'] = int(dates[1])
                except ValueError:
                    if 'Born' in dates:
                        artist['birth_year'] = int(dates.split()[1])
                        artist['death_year'] = None
                except:                        
                    print >>sys.stderr, "ERROR: Can't parse dates for %s: %s" % (artist['name'], artist['alive'])
                    artist['birth_year'] = None
                    artist['death_year'] = None
                artist['profile_link'] = URL + artist['profile_link'][3:]
                try:
                    artist['nationality'], artist['profession'] = artist['artist_type'].split(' ', 1)
                except ValueError:
                    artist['nationality'] = artist['artist_type']
                    artist['profession'] = 'unknown'

                artists.append(artist)
            datastore.save(['name'], table_name="movements", data=dict(name=m['title'], link=m['link']))
            datastore.save(['movement', 'related_to'], table_name="relations", data=relations)
            datastore.save(['name', 'nationality'], table_name="artists", data=artists)

main()

