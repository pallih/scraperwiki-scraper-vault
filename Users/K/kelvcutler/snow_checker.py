import scraperwiki
import lxml.html
import datetime

if (True or datetime.date.today().weekday() == 5):
    html = scraperwiki.scrape("http://www.weather.com/weather/tomorrow/Provo+UT+84601:4:US")
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect("div.wx-details dl"):
        text = " ".join(el.text_content().split())
        if (text.find("Chance of snow:") == 0):
            data = {
                "title":"Chance of Snow",
                "link":"http://www.weather.com/weather/tomorrow/Provo+UT+84601:4:US", 
                "description":text,
                "guid":str(datetime.date.today())+text,
                "date":datetime.date.today(), 
                "chanceOfSnow":text}
            scraperwiki.sqlite.save(unique_keys=["date"], data=data)
            break


