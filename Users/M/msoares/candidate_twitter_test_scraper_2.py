import scraperwiki
import lxml.html
import datetime

candidates = (["joseserra_", "Haddad_Fernando", "celsorussomanno", "SoninhaFrancine", "carlos_giannazi", "gabriel_chalita", "levyfidelix", "Eymaeloficial", "paulinhopdt12"])


date = datetime.date.today()


for candidate_name in candidates:
    url = ("http://twitter.com/" + candidate_name)
    html = scraperwiki.scrape(url)
    raw = lxml.html.fromstring(html)

    for row in raw.cssselect("span#follower_count"):
        print row.text
        data = {
            'date':date,
            'handle': candidate_name,
            'followers':row.text
        }

        scraperwiki.sqlite.save(unique_keys=['date'], data=data)