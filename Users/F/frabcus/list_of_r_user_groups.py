import requests
import scraperwiki
import datetime


def get(url, when):
    html = requests.get(url)
    scraperwiki.sqlite.save(["when"], { "when": when, "html": html.text })

# One off code to get the history from archive.org
#get("http://web.archive.org/web/20100523063224/http://blog.revolutionanalytics.com/local-r-groups.html", datetime.date(2010, 5, 23)) 
#get("http://web.archive.org/web/20100806001622/http://blog.revolutionanalytics.com/local-r-groups.html", datetime.date(2010, 8, 6));
#get("http://web.archive.org/web/20110611085543/http://blog.revolutionanalytics.com/local-r-groups.html", datetime.date(2011, 6, 11))
#get("http://web.archive.org/web/20110715180837/http://blog.revolutionanalytics.com/local-r-groups.html", datetime.date(2011, 7, 15))

# And then get every day
get("http://blog.revolutionanalytics.com/local-r-groups.html", datetime.date.today())
