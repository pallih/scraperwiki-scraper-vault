import scraperwiki
import lxml.html

# defenders
positions = ['DE','MI','FO','RU']
rownames = ["tr[bgcolor='#f2f4f7']", "tr[bgcolor='#ffffff']"]
id = 0
for match in range(1,24):
    for pos in positions:
        print "looking in ", pos
        url = "http://www.footywire.com/afl/footy/dream_team_round?round=" + str(match) + "&p=" + pos + "&s=T"
        print "scraping ", url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        
        for row in rownames:
            print "row type: ", row
            for tr in root.cssselect(row):
                tds = tr.cssselect("td")
                
                data = {
                        'id': id,
                        'round': match,
                        'position' : pos,
                        'name' : tds[1].text_content().split("\n")[0] + "(" + tds[2].text_content() + ")",
                        'score' : tds[4].text_content()
                        }
                
                id += 1
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
        


