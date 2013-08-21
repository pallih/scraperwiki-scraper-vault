import scraperwiki
import datetime
from lxml import etree

# FYI: Day counts began on 3/28/2012

FEED_URL = "http://tfsfrp.tamu.edu/wildfires/BurnBan.xml"
TODAY_DATE = datetime.date.today()

def act_on_matches(matches):
    storage = []

    for match in matches:
        data_obj = scraperwiki.sqlite.select("* from swdata where county=?", match)[0];
        ban_status = data_obj["ban"]
        last_updated_date = data_obj["lastupdated"]
        
        if ban_status == 0:
            data_obj["ban"] = 1
            data_obj["banstartdate"] = TODAY_DATE
            data_obj["banenddate"] = ""
        if TODAY_DATE != last_updated_date:    
            data_obj["consecutive"] += 1
            data_obj["bantotal"] += 1
            data_obj["lastupdated"] = TODAY_DATE
        
        storage.append(data_obj)

    return storage

def act_on_misses(misses):
    storage = []

    for miss in misses:
        data_obj = scraperwiki.sqlite.select("* from swdata where county=?", miss)[0];
        ban_status = data_obj["ban"]

        print ban_status
        
        if ban_status == 1:
            data_obj["ban"] = 0
            data_obj["banstartdate"] = ""
            data_obj["banenddate"] = TODAY_DATE
            data_obj["consecutive"] = 0

        data_obj["lastupdated"] = TODAY_DATE
        
        storage.append(data_obj)
            
    return storage

def data_save(data):
    scraperwiki.sqlite.save(["county"], data)

def prepare_table():
    data = scraperwiki.sqlite.select("* from swdata")
    dataList = []
    
    for entry in data:
        ban_status = entry["ban"]
        if ban_status == 1:
            entry["banenddate"] = ""   
        else:
            entry["banstartdate"] = ""
        
        dataList.append(entry)

    data_save(dataList)

def main():
    today_bans = [x.strip() for x in etree.parse(FEED_URL).getroot().findtext("channel/item/description").split(",")]
    county_list = [county["county"] for county in scraperwiki.sqlite.select("county from swdata")]

    today_set = set(today_bans)
    county_set = set(county_list)
    matches = today_set & county_set
    misses = county_set - today_set
    
    print len(matches)
    print len(misses)
    data = act_on_matches(matches) + act_on_misses(misses)
    
    data_save(data)
main()
