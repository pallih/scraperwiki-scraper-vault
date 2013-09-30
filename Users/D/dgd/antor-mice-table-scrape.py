# Blank Python
import scraperwiki
import BeautifulSoup

#from scraperwiki 
#import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www.antormice.com/en/index.php?b=3')
#http://news.bbc.co.uk/sport2/hi/football/eng_prem/table/default.stm

page = BeautifulSoup.BeautifulSoup(html)

#find rows that contain
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: #[1:]: what does this do?
        if row.get('td')#in ['r1', 'r2']:
            #pos = row.contents[1].string
            #team = row.contents[3].a.string
            #gd = row.contents[-4].string
           # pts = row.contents[-2].string
            print td# pos, team, "gd", gd, "pts", pts
            data = {'td':td}#pos,
                    #'team':team,
                    #'gd':gd,
                    #'pts':pts}
            datastore.save(unique_keys=['td'], data=data)


# Blank Python
import scraperwiki
import BeautifulSoup

#from scraperwiki 
#import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www.antormice.com/en/index.php?b=3')
#http://news.bbc.co.uk/sport2/hi/football/eng_prem/table/default.stm

page = BeautifulSoup.BeautifulSoup(html)

#find rows that contain
for table in page.findAll('table'):
    for row in table.findAll('tr')[1:]: #[1:]: what does this do?
        if row.get('td')#in ['r1', 'r2']:
            #pos = row.contents[1].string
            #team = row.contents[3].a.string
            #gd = row.contents[-4].string
           # pts = row.contents[-2].string
            print td# pos, team, "gd", gd, "pts", pts
            data = {'td':td}#pos,
                    #'team':team,
                    #'gd':gd,
                    #'pts':pts}
            datastore.save(unique_keys=['td'], data=data)


