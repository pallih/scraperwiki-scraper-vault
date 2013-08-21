import scraperwiki
import lxml.html  

steam_app_base_url = "http://store.steampowered.com/app/"

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS gamedata ('ID' string, 'Title' string, 'Genre' string, 'Publisher' string, 'Release_Date' string, PRIMARY KEY('Title'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO gamedata ('ID', 'Title', 'Release_Date', 'Genre', 'Publisher') VALUES (?, ?, ?, ?, ?)", (data['ID'], data['Title'], data['Release_Date'], data['Genre'], data['Publisher']))
    scraperwiki.sqlite.commit()


def scrape():
    global steam_app_base_url;
    gamelist = "http://api.steampowered.com/ISteamApps/GetAppList/v2/?format=xml"
    html = scraperwiki.scrape(gamelist)
    root = lxml.html.fromstring(html)
    for row in root.cssselect("applist apps app"):
        gameID = row.cssselect("appid")[0].text_content()
        appName = row.cssselect("name")[0].text_content()
        if appName.find('Trailer') != -1:
            print 'skipping ' + gameID
            continue
        gameURL = steam_app_base_url + gameID
        try:
            game_html = scraperwiki.scrape(gameURL)
            game_root = lxml.html.fromstring(game_html)
            div = game_root.cssselect(".game_details .block_content .block_content_inner .details_block")
            if len(div) == 0:
                continue
            title = ""
            genre = ""
            release_date = ""
            publisher = ""
            game_details = div[0].text_content()
            list_details = lxml.html.tostring(div[0]).split('<br>')
            for detail in list_details:
                temp = detail.split(':</b>')
                if temp[0].find('Title') != -1:
                    title = temp[1].replace('\r', '').replace('\n', '').replace('\t', '')
                elif temp[0].find('Genre') != -1:
                    genre = lxml.html.fromstring(temp[1].replace('\r', '').replace('\n', '').replace('\t', '')).text_content()
                elif temp[0].find('Publisher') != -1:
                    publisher = lxml.html.fromstring(temp[1].replace('\r', '').replace('\n', '').replace('\t', '')).text_content()
                elif temp[0].find('Release Date') != -1:
                    release_date = temp[1].replace('\r', '').replace('\n', '').replace('\t', '')
            data = {
                 'ID' : gameID,
                 'Title' : title,
                 'Release_Date': release_date,
                 'Genre' : genre,
                 'Publisher' : publisher
            }
            saveToStore(data)
        except Exception, err:
            continue


scrape()