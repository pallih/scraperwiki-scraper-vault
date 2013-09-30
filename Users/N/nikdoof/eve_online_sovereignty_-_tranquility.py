import pickle
import scraperwiki
import xml.etree.ElementTree as et
import dateutil.parser
from datetime import datetime

evecache = scraperwiki.utils.swimport('eve_api_cache_library')

# Get the data
root = evecache.eveapi_get("https://api.eveonline.com/map/Sovereignty.xml.aspx")

# Generate Sov set
sov = [system.attrib for system in root.iter('row')]
scraperwiki.sqlite.save(['solarSystemName'], sov)

corplist = []
allilist = []
for sys in sov:
    if int(sys['allianceID']) > 0:
        allilist.append({'allianceID': int(sys['allianceID']), 'allianceName': ''})
        corplist.append({'corporationID': int(sys['corporationID']), 'corporationName': ''})

scraperwiki.sqlite.save(['allianceID'], allilist, table_name="alliance_list")
scraperwiki.sqlite.save(['corporationID'], corplist, table_name="corporation_list")

import pickle
import scraperwiki
import xml.etree.ElementTree as et
import dateutil.parser
from datetime import datetime

evecache = scraperwiki.utils.swimport('eve_api_cache_library')

# Get the data
root = evecache.eveapi_get("https://api.eveonline.com/map/Sovereignty.xml.aspx")

# Generate Sov set
sov = [system.attrib for system in root.iter('row')]
scraperwiki.sqlite.save(['solarSystemName'], sov)

corplist = []
allilist = []
for sys in sov:
    if int(sys['allianceID']) > 0:
        allilist.append({'allianceID': int(sys['allianceID']), 'allianceName': ''})
        corplist.append({'corporationID': int(sys['corporationID']), 'corporationName': ''})

scraperwiki.sqlite.save(['allianceID'], allilist, table_name="alliance_list")
scraperwiki.sqlite.save(['corporationID'], corplist, table_name="corporation_list")

