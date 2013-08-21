import scraperwiki
import lxml.html

#Scrape Constitution Party Press Releases


# Site is nasty and there are so few
# I hand-collected ids of press releases
ids = [1451,
1432,
1305,
1190,
1184,
1154,
1143,
1106,
1083,
1068,
1060,
1042,
1028,
977,
975,
970]

for id in ids:
    pagename = 'http://www.constitution-party.net/news.php?aid=' + str(id)
    #Scrape the page
    page = scraperwiki.scrape(pagename)
    #Root the page
    pageroot = lxml.html.fromstring(page)
    for d in pageroot.cssselect('div#main_content'):    
        doc = d.text_content()
        date = doc.split('/')[0] + doc.split('/')[1] 
        temp = doc.split('/')[2]
        
        data = {'Date': date, 'Document': doc}
        scraperwiki.sqlite.save(unique_keys = ['Document'], data = data)


