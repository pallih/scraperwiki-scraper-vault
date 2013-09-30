import scraperwiki
import lxml.html
from lxml import etree


url="http://www.lolking.net/champions/"
root = lxml.html.fromstring(scraperwiki.scrape(url))
first_row = True
for row in root.cssselect("table.champion-list tr"):
    #print etree.tostring(row, pretty_print=True)    
    if first_row:
        first_row = False
        continue
    champ_name = row[0].attrib["data-sortval"]
    pickrate = float(row[3].attrib["data-sortval"])
    winrate =  float(row[4].attrib["data-sortval"])
    print "%s:%f,%f" % (champ_name,pickrate,winrate)
    scraperwiki.sqlite.save(unique_keys=["champion"], data={"champion":champ_name, "pickpercent":champ_pct })
import scraperwiki
import lxml.html
from lxml import etree


url="http://www.lolking.net/champions/"
root = lxml.html.fromstring(scraperwiki.scrape(url))
first_row = True
for row in root.cssselect("table.champion-list tr"):
    #print etree.tostring(row, pretty_print=True)    
    if first_row:
        first_row = False
        continue
    champ_name = row[0].attrib["data-sortval"]
    pickrate = float(row[3].attrib["data-sortval"])
    winrate =  float(row[4].attrib["data-sortval"])
    print "%s:%f,%f" % (champ_name,pickrate,winrate)
    scraperwiki.sqlite.save(unique_keys=["champion"], data={"champion":champ_name, "pickpercent":champ_pct })
