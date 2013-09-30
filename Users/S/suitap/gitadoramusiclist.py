import scraperwiki
from pyquery import PyQuery as pq
import unicodedata, re

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` ( `name` text, `bscg` text, `advg` text, `extg` text, `masg` text, `bscb` text, `advb` text, `extb` text, `masb` text, `bscd` text, `advd` text, `extd` text, `masd` text, `is_new` text )")

urlmap = {"new": "http://bemaniwiki.com/index.php?GITADORA%2F%BF%B7%B6%CA%A5%EA%A5%B9%A5%C8",
          "old": "http://bemaniwiki.com/index.php?GITADORA%2F%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8"}
for k, v in urlmap.items():
    table = pq(scraperwiki.scrape(v))
    table = table.find("div#body div.ie5 table.style_table tbody tr")
    for l in table:
        tds = pq(l).find("td")
        if len(tds) <= 10:
            continue
        name = tds.eq(1).text().replace(" (DM:V)", "").replace(" (DM:2nd)", "")
        if name == "Predator's Crypto Pt.2":
            data = {
                "name": name,
                "bscd": tds.eq(2).text().replace("-",""),
                "advd": tds.eq(3).text().replace("-",""),
                "extd": tds.eq(4).text().replace("-",""),
                "masd": tds.eq(5).text().replace("-",""),
                "bscg": tds.eq(6).text().replace("-",""),
                "advg": tds.eq(7).text().replace("-",""),
                "extg": tds.eq(8).text().replace("-",""),
                "masg": tds.eq(9).text().replace("-",""),
                "bscb": tds.eq(10).text().replace("-",""),
                "advb": tds.eq(11).text().replace("-",""),
                "extb": tds.eq(12).text().replace("-",""),
                "masb": tds.eq(13).text().replace("-",""),
                "is_new": k,
            }
        else:
            data = {
                "name": name,
                "bscd": tds.eq(5).text().replace("-",""),
                "advd": tds.eq(6).text().replace("-",""),
                "extd": tds.eq(7).text().replace("-",""),
                "masd": tds.eq(8).text().replace("-",""),
                "bscg": tds.eq(9).text().replace("-",""),
                "advg": tds.eq(10).text().replace("-",""),
                "extg": tds.eq(11).text().replace("-",""),
                "masg": tds.eq(12).text().replace("-",""),
                "bscb": tds.eq(13).text().replace("-",""),
                "advb": tds.eq(14).text().replace("-",""),
                "extb": tds.eq(15).text().replace("-",""),
                "masb": tds.eq(16).text().replace("-",""),
                "is_new": k,
            }

        scraperwiki.sqlite.save(unique_keys=["name"], data=data)

import scraperwiki
from pyquery import PyQuery as pq
import unicodedata, re

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` ( `name` text, `bscg` text, `advg` text, `extg` text, `masg` text, `bscb` text, `advb` text, `extb` text, `masb` text, `bscd` text, `advd` text, `extd` text, `masd` text, `is_new` text )")

urlmap = {"new": "http://bemaniwiki.com/index.php?GITADORA%2F%BF%B7%B6%CA%A5%EA%A5%B9%A5%C8",
          "old": "http://bemaniwiki.com/index.php?GITADORA%2F%B5%EC%B6%CA%A5%EA%A5%B9%A5%C8"}
for k, v in urlmap.items():
    table = pq(scraperwiki.scrape(v))
    table = table.find("div#body div.ie5 table.style_table tbody tr")
    for l in table:
        tds = pq(l).find("td")
        if len(tds) <= 10:
            continue
        name = tds.eq(1).text().replace(" (DM:V)", "").replace(" (DM:2nd)", "")
        if name == "Predator's Crypto Pt.2":
            data = {
                "name": name,
                "bscd": tds.eq(2).text().replace("-",""),
                "advd": tds.eq(3).text().replace("-",""),
                "extd": tds.eq(4).text().replace("-",""),
                "masd": tds.eq(5).text().replace("-",""),
                "bscg": tds.eq(6).text().replace("-",""),
                "advg": tds.eq(7).text().replace("-",""),
                "extg": tds.eq(8).text().replace("-",""),
                "masg": tds.eq(9).text().replace("-",""),
                "bscb": tds.eq(10).text().replace("-",""),
                "advb": tds.eq(11).text().replace("-",""),
                "extb": tds.eq(12).text().replace("-",""),
                "masb": tds.eq(13).text().replace("-",""),
                "is_new": k,
            }
        else:
            data = {
                "name": name,
                "bscd": tds.eq(5).text().replace("-",""),
                "advd": tds.eq(6).text().replace("-",""),
                "extd": tds.eq(7).text().replace("-",""),
                "masd": tds.eq(8).text().replace("-",""),
                "bscg": tds.eq(9).text().replace("-",""),
                "advg": tds.eq(10).text().replace("-",""),
                "extg": tds.eq(11).text().replace("-",""),
                "masg": tds.eq(12).text().replace("-",""),
                "bscb": tds.eq(13).text().replace("-",""),
                "advb": tds.eq(14).text().replace("-",""),
                "extb": tds.eq(15).text().replace("-",""),
                "masb": tds.eq(16).text().replace("-",""),
                "is_new": k,
            }

        scraperwiki.sqlite.save(unique_keys=["name"], data=data)

