import scraperwiki   
import lxml.html     
        
html = scraperwiki.scrape("http://www.letsplaysoccer.com/main/locations/northwest/std/nw1schedule.htm")

#print html


root = lxml.html.fromstring(html)
#for tr in root.cssselect("table tr"):
tr = root.cssselect("table tr");
tds = tr[0].cssselect("td")
print tds[0].text_content()
#print tds[1].text_content()
print tds[2].text_content()
#print tds[3].text_content()
print tds[4].text_content()
#print tds[5].text_content()
print tds[6].text_content()
#print tds[7].text_content()
print tds[8].text_content()
#print tds[9].text_content()
print tds[10].text_content()
#print tds[11].text_content()
print tds[12].text_content()
#print tds[13].text_content()
print tds[14].text_content()
#print tds[15].text_content()


ts1a = tr[2].cssselect("td");
ts1b = tr[3].cssselect("td");

game1 = {
    'id' : 1,
    'time' : ts1a[0].text_content(),
    'division' : ts1b[0].text_content(),
    'team1' : ts1a[1].text_content(),
    'team2' : ts1b[1].text_content()
}
print game1
scraperwiki.sqlite.save(unique_keys=['id'], data=game1)

game2 = {
    'time' : ts1a[3].text_content(),
    'division' : ts1b[3].text_content(),
    'team1' : ts1a[4].text_content(),
    'team2' : ts1b[4].text_content()
}

print game2