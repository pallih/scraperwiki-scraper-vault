import lxml.html
import re
import scraperwiki

pattern = re.compile(r'\s')
html = scraperwiki.scrape("http://www.shanghairanking.com/ARWU2012.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("#UniversityRanking tr:not(:first-child)"):
    if len(tr.cssselect("td.ranking")) > 0 and len(tr.cssselect("td.rankingname")) > 0:
        data = {
            'arwu_rank'  : str(re.sub(pattern, r'', tr.cssselect("td.ranking")[0].text_content())),
            'university' : tr.cssselect("td.rankingname")[0].text_content().strip()
        }
    print data
    # DEBUG BEGIN
#    if not type(data["arwu_rank"]) is str:
#        print type(data["arwu_rank"])
#        print data["arwu_rank"]
#        print data["university"]
    # DEBUG END
    if "-" in data["arwu_rank"]:
        arwu_rank_bounds  = data["arwu_rank"].split("-")
        data["arwu_rank"] = int( ( float(arwu_rank_bounds[0]) + float(arwu_rank_bounds[1]) ) * 0.5 )
    if not type(data["arwu_rank"]) is int:
        data["arwu_rank"] = int(data["arwu_rank"])
    scraperwiki.sqlite.save(unique_keys=['university'], data=data)import lxml.html
import re
import scraperwiki

pattern = re.compile(r'\s')
html = scraperwiki.scrape("http://www.shanghairanking.com/ARWU2012.html")
root = lxml.html.fromstring(html)
for tr in root.cssselect("#UniversityRanking tr:not(:first-child)"):
    if len(tr.cssselect("td.ranking")) > 0 and len(tr.cssselect("td.rankingname")) > 0:
        data = {
            'arwu_rank'  : str(re.sub(pattern, r'', tr.cssselect("td.ranking")[0].text_content())),
            'university' : tr.cssselect("td.rankingname")[0].text_content().strip()
        }
    print data
    # DEBUG BEGIN
#    if not type(data["arwu_rank"]) is str:
#        print type(data["arwu_rank"])
#        print data["arwu_rank"]
#        print data["university"]
    # DEBUG END
    if "-" in data["arwu_rank"]:
        arwu_rank_bounds  = data["arwu_rank"].split("-")
        data["arwu_rank"] = int( ( float(arwu_rank_bounds[0]) + float(arwu_rank_bounds[1]) ) * 0.5 )
    if not type(data["arwu_rank"]) is int:
        data["arwu_rank"] = int(data["arwu_rank"])
    scraperwiki.sqlite.save(unique_keys=['university'], data=data)