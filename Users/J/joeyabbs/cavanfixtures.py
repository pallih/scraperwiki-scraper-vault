import lxml.html
import scraperwiki

url = "http://www.sportsmanager.ie/t7.php?countyid=4&sportid=1&club_id=&defaultpage=1&userid=6933"
root = lxml.html.parse(url).getroot()

print "The root element is:", root
print "The elements in this root element are:", list(root)
print "The elements two levels down are:", [ list(el)  for el in root ]

divs = root.cssselect("div")
print "There are %d elements with tag div in this page" % len(divs)
print "Their corresponding attributes are:", [div.attrib  for div in divs ]

comp = ""
for el in root.cssselect("table tr.reportrow"):
    if el.cssselect(".reportrow_competition_name"):
        comp = el[0].text.strip()
        #print "===%s===" % comp
    else:
        home_team = el[0].text.strip()
        away_team = el[1].text.strip()
        if away_team == "Ballinagh" or home_team == "Ballinagh":
            print "===%s===" % comp
            print "%s vs %s" % (home_team, away_team)
            data1 = { "comp":comp, "home_team":home_team, "away_team":away_team }
            scraperwiki.sqlite.save(unique_keys=["comp"], data=data1)
        
#data1 = { "comp":comp, "home_team":home_team, "away_team":away_team }
#scraperwiki.sqlite.save(unique_keys=["comp"], data=data1)
print scraperwiki.sqlite.select("* from swdata")

rows = root.cssselect("tr.reportrow")
print "There are %d reportrow elements in this page" % len(rows)

