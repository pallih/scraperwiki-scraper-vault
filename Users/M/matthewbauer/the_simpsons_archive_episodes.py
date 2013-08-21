# The Simpsons Archive
# snpp.com

import scraperwiki
import lxml.html
import re

html = scraperwiki.scrape("http://www.snpp.com/episodes.html")
root = lxml.html.fromstring(html)

rows = root.xpath("body/*/tr")

current_season = {}

for row in rows:
    # is section title?
    if row.xpath("td[@width='600'][@height='30']/center/b/text()") != []:
        current_season = {}
        current_season['section'] = row.xpath("td[@width='600'][@height='30']/center/b/text()")[0]
    # is season title?
    elif row.xpath("td[@align='right'][@width='300']/font/b/text()") != []:
        current_season['name'] = row.xpath("td[1]/font/b/text()")[0]
        current_season['year'] = row.xpath("td[@align='right']/font/b/text()")[0]
    # is episode?
    elif current_season and row.xpath("td/font[@size='2']") != []:
        episode = {}

        td = row.xpath("td[font[@size='2']]")[0]
        col1_width = int(td.get('width'))
        if col1_width == 45:
            col2_width = 470
        elif col1_width == 50:
            col2_width = 410
        elif col1_width == 65:
            col2_width = 450
        else:
            continue

        episode['season_section'] = current_season['section']
        episode['season_year'] = current_season['year']
        episode['season_name'] = current_season['name']

        if row.xpath("td[@width='%i']/font[@size='2']/a" % col1_width) != []:
            episode['number'] = row.xpath("td[@width='%i']/font[@size='2']/a/text()" % col1_width)[0]
            episode['url'] = "http://www.snpp.com/%s" % row.xpath("td[@width='%i']/font[@size='2']/a/@href" % col1_width)[0]
        else:
            episode['number'] = row.xpath("td[@width='%i']/font[@size='2']/text()" % col1_width)[0]
            episode['url'] = "http://www.snpp.com/404"

        episode['title'] = row.xpath("td[@width='%i']/text()" % col2_width)[0]
        episode['air_date'] = row.xpath("td[@align='right']/font/text()")[0]
        scraperwiki.sqlite.save(unique_keys=['title', 'number', 'air_date'], data=episode)

