import scraperwiki
import lxml.html
from time import time

for i in range(463,464):
    max_attempts = 8
    for attempts in range(max_attempts):
        try:
            url = "http://games.crossfit.com/scores/leaderboard.php?stage=5&sort=0&page=%s&division=1&region=0&numberperpage=100&competition=0&frontpage=0&expanded=0&year=13&full=1&showtoggles=0&hidedropdowns=1&showathleteac=1&=%s" % (i,time())
            agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
            html = scraperwiki.scrape(url,user_agent=agent)
            break
        except scraperwiki.Error, e:
            sleep_secs = attempts ** 3
            time.sleep(sleep_secs)

    athletes_links = []

    root = lxml.html.fromstring(html)
    for trs in root.cssselect("table[id='lbtable'] tbody tr"):
        tds = trs.cssselect("td")
        if len(tds) == 7:
            athlete = {}
            athlete['rank'] = tds[0].text_content()
            athlete['link'] = tds[1].cssselect("a")[0].attrib["href"]
            athletes_links.append(athlete)

    for athlete_link in athletes_links:
        lmax_attempts = 8
        for attempt in range(lmax_attempts):
            try:
                athlete_html = scraperwiki.scrape(athlete_link['link'])
                break
            except scraperwiki.Error, e:
                lsleep_secs = lmax_attempts ** 3
                time.sleep(lsleep_secs)
        athlete_root = lxml.html.fromstring(athlete_html)
        try:
            athlete['name'] = athlete_root.xpath("//h2[@id='page-title']/text()")[0]
        except IndexError:
            athlete['name'] = "none"
        athlete['rank'] = athlete_link['rank']
        info = athlete_root.xpath("//dl/dd/text()")
        area = athlete_root.xpath("//dl/dd/a/text()")
    
        if len(area) == 3:
            athlete['region'] = area[0]
            athlete['team']  = area[1]
            athlete['affiliate'] = area[2]
        elif len(area) == 2:
            athlete['region'] = area[0]
            athlete['team'] = "none"
            athlete['affiliate'] = area[1]
        elif len(area) == 1:
            athlete['region'] = area[0]
            athlete['team'] = "none"
            athlete['affiliate'] = "none"
        else:
            athlete['region'] = "none"
            athlete['team'] = "none"
            athlete['affiliate'] = "none"

        if len(info) == 4:
            athlete['sex'] = info[0]
            athlete['age'] = info[1]
            athlete['height'] = info[2]
            athlete['weight'] = info[3]
        else:
            athlete['sex'] = "none"
            athlete['age'] = "none"
            athlete['height'] = "none"
            athlete['weight'] = "none"   

        tabs = athlete_root.xpath("//div[@class='profile-stats']/table")
        for tab in tabs:
            if len(tab) > 0:
                for tr in tab:
                    if len(tr) == 2:
                        athlete[tr[0].text_content().replace(" ","").replace("&","")] = tr[1].text_content()

        smax_attempts = 8
        for attempt in range(smax_attempts):
            try:
                scraperwiki.sqlite.save(unique_keys=['name'], data=athlete)
                break
            except scraperwiki.Error, e:
                ssleep_secs = smax_attempts ** 3
                time.sleep(ssleep_secs)