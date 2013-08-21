import scraperwiki
import datetime

now = datetime.datetime.now()

partier = (["veja", "g1", "folhadesp"]);

count = 1

for i in partier:
    url = ("https://graph.facebook.com/" + i + "?fields=likes")

    html = scraperwiki.scrape(url)

    import re

    start = html.find(':')+1
    end = html.find(',', start)
    m=html[start:end]
    print m

    data = {'RowId': count, 'Likes': m,'Parti': i, 'Time': now}


    print count
    count += 1

    scraperwiki.sqlite.save(unique_keys=['RowId', 'Time'], data=data)
