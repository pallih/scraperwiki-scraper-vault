import scraperwiki
import lxml.html
import datetime

for name in ["NXTBoy", "Telamon", "Builderman", "Roblox", "xLEGOx", "Anaminus"]:
    html = scraperwiki.scrape("http://www.roblox.com/User.aspx?username="+name)
    root = lxml.html.fromstring(html)
    
    profileContainer = root.cssselect("#ctl00_cphRoblox_rbxUserStatisticsPane_lProfileViewsStatistics")
    
    profileViews = profileContainer[0].text_content().replace(',', '')
    
    if len(profileContainer) > 0:
        profileViews = int(profileViews)
        
        
        scraperwiki.sqlite.save(unique_keys=['name', 'checked_on'], data={
            'name':name,
            'checked_on': datetime.datetime.utcnow(),
            'views' : profileViews
        })
        
        print profileViews
    else:
        print "Uh oh..."