import scraperwiki
from lxml import etree

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS steam_gamestats ('User ID' string, 'Game' string, 'Hours_Played' real, PRIMARY KEY('User ID', 'Game'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO steam_gamestats ('User ID', 'Game', 'Hours_Played') VALUES (?, ?, ?)", (data['User_ID'], data['Game'], data['Hours_Played']))
    scraperwiki.sqlite.commit()

def scrape(url):
    try:
        tree = etree.parse(url + "/games?xml=1")
        id = tree.xpath('/gamesList/steamID64')[0].text
        games = tree.xpath('/gamesList/games/game')
        for game in games:
            game_title = game.xpath('name')[0].text
            hours_played = float(game.xpath('hoursOnRecord')[0].text)
            data = {
                'User_ID'      : id,
                'Game'         : game_title,
                'Hours_Played' : hours_played
            }
            saveToStore(data)
        return 1
    except Exception, err:
        return 0

def start():
    scraperwiki.sqlite.attach("get_steam_user_profile_pages", "src")
    results = scraperwiki.sqlite.select("URL from src.userpages order by UserName DESC")
    for row in results:
        scrape(row['URL'])

start()import scraperwiki
from lxml import etree

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS steam_gamestats ('User ID' string, 'Game' string, 'Hours_Played' real, PRIMARY KEY('User ID', 'Game'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO steam_gamestats ('User ID', 'Game', 'Hours_Played') VALUES (?, ?, ?)", (data['User_ID'], data['Game'], data['Hours_Played']))
    scraperwiki.sqlite.commit()

def scrape(url):
    try:
        tree = etree.parse(url + "/games?xml=1")
        id = tree.xpath('/gamesList/steamID64')[0].text
        games = tree.xpath('/gamesList/games/game')
        for game in games:
            game_title = game.xpath('name')[0].text
            hours_played = float(game.xpath('hoursOnRecord')[0].text)
            data = {
                'User_ID'      : id,
                'Game'         : game_title,
                'Hours_Played' : hours_played
            }
            saveToStore(data)
        return 1
    except Exception, err:
        return 0

def start():
    scraperwiki.sqlite.attach("get_steam_user_profile_pages", "src")
    results = scraperwiki.sqlite.select("URL from src.userpages order by UserName DESC")
    for row in results:
        scrape(row['URL'])

start()