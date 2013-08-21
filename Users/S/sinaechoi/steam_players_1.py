import scraperwiki
from lxml import etree

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS steam_players ('ID' string, 'Location' string, 'Joined_Date' string, 'Real_Name' string, PRIMARY KEY('ID'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO steam_players ('ID', 'Location', 'Joined_Date', 'Real_Name') VALUES (?, ?, ?, ?)", (data['ID'], data['Location'], data['Joined_Date'], data['Real_Name']))
    scraperwiki.sqlite.commit()

def scrape(url):
    try:
        # data parsing
        tree = etree.parse(url + "?xml=1")
        id = tree.xpath('/profile/steamID64')[0].text

        # define variable
        location = ''
        joined_date = ''
        real_name = ''

        # data read
        if len(tree.xpath('/profile/location')) == 1:
            location = tree.xpath('/profile/location')[0].text
        if len(tree.xpath('/profile/memberSince')) == 1:
            joined_date = tree.xpath('/profile/memberSince')[0].text
        if len(tree.xpath('/profile/realname')) == 1:
            real_name = tree.xpath('/profile/realname')[0].text

        # define array
        data =
        {
            'ID'          : id,
            'Location'    : location,
            'Joined_Date' : joined_date,
            'Real_Name' : real_name
        }

        # save data to database
        saveToStore(data)

        return 1

    except Exception, err:
        return 0

def start():
    scraperwiki.sqlite.attach("get_steam_user_profile_pages", "src")
    results = scraperwiki.sqlite.select("URL from src.userpages")
    for row in results:
        scrape(row['URL'])

start()