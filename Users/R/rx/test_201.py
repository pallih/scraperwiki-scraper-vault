import scraperwiki
import lxml.html
'''
html = scraperwiki.scrape("http://steamcommunity.com/id/Manuuel/games?xml=1")
root = lxml.html.fromstring(html)
sindex = html.index("gamesList")+10
eindex = html.rindex("gamesList")
bodycontent = html[sindex:eindex]
sindex = bodycontent.index("games")+6
eindex = bodycontent.rindex("games")-2
rows = bodycontent[sindex:eindex]
print rows
start = rows.index("<game>")
end = rows.index("</game>")
glist = rows.split("<game>")
i=0
for g in glist:
    start = g.find("<name>")
    end = g.find("</name>")
    start2 = g.find("<hoursOnRecord>")
    end2 = g.find("</hoursOnRecord>")
    if start!=-1 and end!=-1:
        i=i+1
        name = g[start+6:end]
        #hours = g[start2+15:end]
        print name[9:len(name)-3]
        if start2==-1 or end2==-1:
            hours = 0.0
        else:
            hours = float(g[start2+15:end2])
        print hours
'''
html = scraperwiki.scrape("http://steamcommunity.com/id/Manuuel?xml=1")
root = lxml.html.fromstring(html)
location = root.cssselect("location")[0].text_content()
print location
    



