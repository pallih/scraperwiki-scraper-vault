import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://news.bbc.co.uk/sport2/hi/football/eng_prem/table/default.stm')
#http://news.bbc.co.uk/sport2/hi/football/eng_prem/table/default.stm

page = BeautifulSoup.BeautifulSoup(html)

#find rows that contain
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: #[1:]: what does this do?
        if row.get('class','') in ['r1', 'r2']:
            pos = row.contents[1].string
            team = row.contents[3].a.string
            gd = row.contents[-4].string
            pts = row.contents[-2].string
            print pos, team, "gd", gd, "pts", pts
            data = {'pos':pos,
                    'team':team,
                    'gd':gd,
                    'pts':pts}
            datastore.save(unique_keys=['team'], data=data)



