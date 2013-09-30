import scraperwiki

mac_list = scraperwiki.scrape("http://standards.ieee.org/develop/regauth/oui/oui.txt")
ouiDict = {}

entries = mac_list.split("\n\n")[1:-1]
for entry in entries:
    parts = entry.split("\n")[1].split("\t")
    company_id = parts[0].split()[0]
    company_name = parts[-1]
    ouiDict[company_id] = company_name

for key, value in ouiDict.iteritems() :
    data = {'MAC address' : key, 'Manufacturer' : value}
    scraperwiki.sqlite.save(unique_keys=['MAC address'], data=data)
import scraperwiki

mac_list = scraperwiki.scrape("http://standards.ieee.org/develop/regauth/oui/oui.txt")
ouiDict = {}

entries = mac_list.split("\n\n")[1:-1]
for entry in entries:
    parts = entry.split("\n")[1].split("\t")
    company_id = parts[0].split()[0]
    company_name = parts[-1]
    ouiDict[company_id] = company_name

for key, value in ouiDict.iteritems() :
    data = {'MAC address' : key, 'Manufacturer' : value}
    scraperwiki.sqlite.save(unique_keys=['MAC address'], data=data)
