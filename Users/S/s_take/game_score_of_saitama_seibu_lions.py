# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def get_score(source):
    score = {}
    score["team"] = source[0].img["alt"]
    for i in range(1, 13):
        score[i] = source[i].a.text
    score["r"] = source[13].text
    score["h"] = source[14].text
    score["e"] = source[15].text
    return score

def store_score(score, is_bottom):
    team_id = 1 if is_bottom else 0
    team = {
        "id": team_id,
        "name": score["team"],
        "runs": score["r"],
        "hits": score["h"],
        "errors": score["e"]
    }
    scraperwiki.sqlite.save(["id"], team, table_name="teams")
    for i in range(1, 13):
        inning_score = {
            "inning": i,
            "team": team_id,
            "runs": score[i]
        }
        scraperwiki.sqlite.save(["inning", "team"], inning_score, table_name="innings")

url = "http://www.seibulions.jp/game/scoreboard/"
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
source = soup.findAll("td", attrs={"class": ["tdLogo", "tdScore"]})
store_score(get_score(source[0:16]), False)
store_score(get_score(source[16:32]), True)
# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

def get_score(source):
    score = {}
    score["team"] = source[0].img["alt"]
    for i in range(1, 13):
        score[i] = source[i].a.text
    score["r"] = source[13].text
    score["h"] = source[14].text
    score["e"] = source[15].text
    return score

def store_score(score, is_bottom):
    team_id = 1 if is_bottom else 0
    team = {
        "id": team_id,
        "name": score["team"],
        "runs": score["r"],
        "hits": score["h"],
        "errors": score["e"]
    }
    scraperwiki.sqlite.save(["id"], team, table_name="teams")
    for i in range(1, 13):
        inning_score = {
            "inning": i,
            "team": team_id,
            "runs": score[i]
        }
        scraperwiki.sqlite.save(["inning", "team"], inning_score, table_name="innings")

url = "http://www.seibulions.jp/game/scoreboard/"
html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)
source = soup.findAll("td", attrs={"class": ["tdLogo", "tdScore"]})
store_score(get_score(source[0:16]), False)
store_score(get_score(source[16:32]), True)
