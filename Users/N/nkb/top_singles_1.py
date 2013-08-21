import scraperwiki
import lxml.html


def scrape_page_and_get_next(id, page, week, year):
    
    year_string = str(year)
    year_string = year_string[2:]

    week_string =  str(week)
    
    if (week < 10):
        week_string = "0" +  str(week)

    url = "http://www.chartsinfrance.net/charts/"+ year_string + week_string +"/singles.php,p"+ str(page)
        
    html = scraperwiki.scrape(url).decode('latin-1', 'replace')
    
    root = lxml.html.fromstring(html)
    
    for item in root.cssselect("div[class='b572']"):
        
        id = id+1
    
        #fetches the ranking
        ranking_raw = item.cssselect("div[class='c1_td2']")
        ranking = ranking_raw[0].text
        
        #fetches artist
        artist_raw = item.cssselect("font[class='noir13b']")
        artist = artist_raw[0].text
        
        #case when there's a link
        if (artist == None):
            artist_raw = artist_raw[0].cssselect("a")
            artist = artist_raw[0].text
        
        #fetches song
        song_raw = item.cssselect("font[class='noir11']")
        song = song_raw[0].text
    
        #case when there's a link
        if (song == None):
            song_raw = song_raw[0].cssselect("a")
            song = song_raw[0].text
    
        data = {
              'id' : id,
              'year' : year,
              'week' : week,
              'song' : song,
              'artist' : artist,
              'ranking' : int(ranking)
        
            }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
    #gets next
    if (page<3):
        page = page + 1
        scrape_page_and_get_next(id, page, week, year)
    else:
        week = week + 1
        change_week(id, week, year)
    

def change_year(id, year):

    scrape_page_and_get_next(id, 1, 1, year)
    

def change_week(id, week, year):
    
    if (week>52):
        year = year + 1
        change_year(id, year)
    
    scrape_page_and_get_next(id, 1, week, year)

if(scraperwiki.sqlite.execute("select * from swdata where id = (select max(id) from swdata);")):

    last_row = scraperwiki.sqlite.execute("select * from swdata where id = (select max(id) from swdata);")

    id = last_row["data"][0][5] + 1
    
    page = 1
    
    year= last_row["data"][0][4]
    
    week = last_row["data"][0][0]

else:
    id = 0
    year = 1984
    week = 44

scrape_page_and_get_next(id, 1, week, year)
    