# coding: utf-8
import scraperwiki
from pyquery import PyQuery as pq
import unicodedata, re

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` ( `sn_name` text, `sn_isnew` text, `sn_novg` text, `sn_regg` text, `sn_expg` text, `sn_masg` text, `sn_novb` text, `sn_regb` text, `sn_expb` text, `sn_masb` text, `sn_novd` text, `sn_regd` text, `sn_expd` text, `sn_masd` text, `ga_name` text, `nz_name` text)")

def normalize(text):
    normalized = unicodedata.normalize("NFKC", unicode(re.sub("\\s", "", text)))
    normalized = normalized.replace(u"Ё", "E").replace(u"Φ", "O").replace(u"　", "").replace(u" ", "")
    normalized = normalized.replace("WILDCREATURES", "WILDCREATRURES")
    normalized = normalized.lower()
    return normalized

def setup_gate_titles():
    gate_titles = {};
    def setup_gate_title(title):
        gate_titles[normalize(title.text)] = title.text
    for i in range(14):
        html = scraperwiki.scrape("http://p.eagate.573.jp/game/gfdm/xg3/gf/p/ranking/music.html?cat={}".format(i)).decode("shift_jis")
        for title in pq(html).find("div.ranking_title"):
            setup_gate_title(title)
    gate_titles[u"dependonme"] = "Depend on me"
    return gate_titles

def lookup_gate_titles(title):
    return gate_titles.get(normalize(title), None)

def scrape_skillnote(new_or_old):
    html = scraperwiki.scrape("http://xv-s.heteml.jp/skill/music_xg3.php?k={}".format(new_or_old))
    table = pq(html)
    table = table.find("table").eq(1).remove("tr:lt(2)").find("tr")
    for l in table:
        tds = pq(l).find("td")
        data = {
            "sn_name": tds.eq(0).text(),
            "sn_novd": tds.eq(2).text(),
            "sn_regd": tds.eq(3).text(),
            "sn_expd": tds.eq(4).text(),
            "sn_masd": tds.eq(5).text(),
            "sn_novg": tds.eq(6).text(),
            "sn_regg": tds.eq(7).text(),
            "sn_expg": tds.eq(8).text(),
            "sn_masg": tds.eq(9).text(),
            "sn_novb": tds.eq(10).text(),
            "sn_regb": tds.eq(11).text(),
            "sn_expb": tds.eq(12).text(),
            "sn_masb": tds.eq(13).text(),
            "sn_isnew": ("new" == new_or_old),
            "ga_name": lookup_gate_titles(tds.eq(0).text()),
            "nz_name": normalize(tds.eq(0).text()),
        }
        scraperwiki.sqlite.save(unique_keys=["sn_name"], data=data)



gate_titles = setup_gate_titles()

for mode in ("new", "old"):
    scrape_skillnote(mode)

# coding: utf-8
import scraperwiki
from pyquery import PyQuery as pq
import unicodedata, re

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` ( `sn_name` text, `sn_isnew` text, `sn_novg` text, `sn_regg` text, `sn_expg` text, `sn_masg` text, `sn_novb` text, `sn_regb` text, `sn_expb` text, `sn_masb` text, `sn_novd` text, `sn_regd` text, `sn_expd` text, `sn_masd` text, `ga_name` text, `nz_name` text)")

def normalize(text):
    normalized = unicodedata.normalize("NFKC", unicode(re.sub("\\s", "", text)))
    normalized = normalized.replace(u"Ё", "E").replace(u"Φ", "O").replace(u"　", "").replace(u" ", "")
    normalized = normalized.replace("WILDCREATURES", "WILDCREATRURES")
    normalized = normalized.lower()
    return normalized

def setup_gate_titles():
    gate_titles = {};
    def setup_gate_title(title):
        gate_titles[normalize(title.text)] = title.text
    for i in range(14):
        html = scraperwiki.scrape("http://p.eagate.573.jp/game/gfdm/xg3/gf/p/ranking/music.html?cat={}".format(i)).decode("shift_jis")
        for title in pq(html).find("div.ranking_title"):
            setup_gate_title(title)
    gate_titles[u"dependonme"] = "Depend on me"
    return gate_titles

def lookup_gate_titles(title):
    return gate_titles.get(normalize(title), None)

def scrape_skillnote(new_or_old):
    html = scraperwiki.scrape("http://xv-s.heteml.jp/skill/music_xg3.php?k={}".format(new_or_old))
    table = pq(html)
    table = table.find("table").eq(1).remove("tr:lt(2)").find("tr")
    for l in table:
        tds = pq(l).find("td")
        data = {
            "sn_name": tds.eq(0).text(),
            "sn_novd": tds.eq(2).text(),
            "sn_regd": tds.eq(3).text(),
            "sn_expd": tds.eq(4).text(),
            "sn_masd": tds.eq(5).text(),
            "sn_novg": tds.eq(6).text(),
            "sn_regg": tds.eq(7).text(),
            "sn_expg": tds.eq(8).text(),
            "sn_masg": tds.eq(9).text(),
            "sn_novb": tds.eq(10).text(),
            "sn_regb": tds.eq(11).text(),
            "sn_expb": tds.eq(12).text(),
            "sn_masb": tds.eq(13).text(),
            "sn_isnew": ("new" == new_or_old),
            "ga_name": lookup_gate_titles(tds.eq(0).text()),
            "nz_name": normalize(tds.eq(0).text()),
        }
        scraperwiki.sqlite.save(unique_keys=["sn_name"], data=data)



gate_titles = setup_gate_titles()

for mode in ("new", "old"):
    scrape_skillnote(mode)

