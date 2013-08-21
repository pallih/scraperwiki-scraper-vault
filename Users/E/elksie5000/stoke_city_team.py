import scraperwiki
import lxml.html
import urllib
import time
from time import mktime
from datetime import date, timedelta, datetime


date = date.today()
url = "http://www.stokecityfc.com/team/"
search_firstblock ="http://www.thisisstaffordshire.co.uk/search/search.html?searchPhrase="
search_secondblock = "&where=&searchType=&orderByOption=dateDesc"

html = scraperwiki.scrape(url)
print html

root = lxml.html.fromstring(html)

player_profile = root.cssselect("ul.team_players li li.player_name")
for player in player_profile:
    count = 0
    player_name = player.text_content()
    player_name_lower = player_name.lower()
    #player_nospace = player_name_lower.encode()
    player_nospace = player_name.replace(" ", "+")
    #player_encoded = urllib.quote(player_nospace)
    url_search = search_firstblock+player_nospace+search_secondblock
    print url_search
    today_date = datetime.today()
    seven_days = timedelta(7) #what is the datetime object for 30 days
    seven_days_ago = today_date - seven_days #what is the dateobject for 30 days ago
    search_html = scraperwiki.scrape(url_search)
    search_root = lxml.html.fromstring(search_html)
    date_article = search_root.xpath("/html/body/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li/div/div/div/div[2]/span[2]/span[2]")
    for date_one in date_article:
        date_bit = date_one.text_content()
        date_noday = date_bit.split(", ")
        #print date_noday[1]
        date_compare = time.strptime(date_noday[1], "%B %d %Y")
        dt = datetime.fromtimestamp(mktime(date_compare))
        #print dt.__class__
        if dt > seven_days_ago:
            count += 1
    print player_name, count    
    record = {}
    record['Player'] = player_name
    record['Count'] = count
    record['Link'] = url_search
    record['HTML'] = '<h3><a href="'+url_search+'">'+player_name+'</a></h3>'
    scraperwiki.sqlite.save(['Player'], record)


