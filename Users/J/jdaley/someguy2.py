import scraperwiki
html = scraperwiki.scrape("http://hoopdata.com/boxscores.aspx")



import lxml.html
root = lxml.html.fromstring(html)
for team in root.cssselect('table.MyGridView tr'):
    print team.text
    #print lxml.html.tostring(td)
    

##scraperwiki.datastore.save(unique_keys=['toob'], data=data) 


    
