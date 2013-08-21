import scraperwiki
import json
from datetime import date

for i in range(1,1000):
    try:
        jsonPage = scraperwiki.scrape('http://fantasy.premierleague.com/web/api/elements/%d/'%(i))
        playerObj = json.loads(jsonPage)
        data = {}
        data["code"] = playerObj["code"]
        data["transfers_balance"] = playerObj["transfers_balance"]
        data["news_updated"] = playerObj["news_updated"]
        data["news_added"] = playerObj["news_added"]
        data["web_name"] = playerObj["web_name"]
        data["in_dreamteam"] = playerObj["in_dreamteam"]
        data["id"] = playerObj["id"]
        data["first_name"] = playerObj["first_name"]
        data["transfers_out_event"] = playerObj["transfers_out_event"]
        data["selected"] = playerObj["selected"]
        data["total_points"] = playerObj["total_points"]
        data["type_name"] = playerObj["type_name"]
        data["team_name"] = playerObj["team_name"]
        data["status"] = playerObj["status"]
        data["added"] = playerObj["added"]
        data["now_cost"] = playerObj["now_cost"]
        data["transfers_in"] = playerObj["transfers_in"]
        data["news"] = playerObj["news"]
        data["news_return"] = playerObj["news_return"]
        data["transfers_in_event"] = playerObj["transfers_in_event"]
        data["selected_by"] = playerObj["selected_by"]
        data["second_name"] = playerObj["second_name"]
        
        data["date_downloaded"] = date.today()
        scraperwiki.sqlite.save(unique_keys=["id", "date_downloaded"], data=data)
    except:
        print 'Stopped at %d'%(i)
        break