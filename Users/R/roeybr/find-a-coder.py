import scraperwiki
import scraperwiki           
import lxml.html 

url_format = "http://stackoverflow.com/users?page={0}&tab=reputation&filter=quarter"

for page in range(1,1000):
    url = "http://stackoverflow.com/users?page="+str(page)+"&tab=reputation&filter=month"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for info in root.cssselect("div[class='user-info  user-hover']"):  
        for details in info.cssselect("div[class='user-details']"):
            for location in details.cssselect("span[class='user-location']"):
                loc = location.text_content().lower()
                if loc.find("israel") != -1:
                    for tag in info.cssselect("div[class='user-tags']"):
                        print(tag.text_content())
                        if tag.text_content().lower().find("php") != -1:
                            for profile in details.cssselect("a"):                    
                                data = {
                                    'link': "http://www.stackoverflow.com/"+profile.get("href"),
                                }
                                scraperwiki.sqlite.save(unique_keys=['link'],data=data)
                                break
                            break


    

