import scraperwiki
import lxml.html

import pytz
from datetime import datetime

def scrape_page(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    london = pytz.timezone('Europe/London')

    now_utc = datetime.now(pytz.timezone('UTC'))
    now_tz = now_utc.astimezone(london)

    for whatson in root.cssselect(".whatson"):
        title = whatson.cssselect("h2")[0].text_content().strip()
        date_str = whatson.cssselect(".date")[0].text_content().strip()

        when = datetime.strptime(date_str, "%d%b")
        when = when.replace(year=now_tz.year)

        # We assume here they won't publish things more than 6 months
        # in the past or in the future.
        if when.month - now_tz.month >= 6 :
            when = when.replace(year=now_tz.year-1)
        elif now_tz.month - when.month >= 6:
            when = when.replace(year=now_tz.year+1)

        event = {
            'title': title,
            'date': when.date(),
        }

        scraperwiki.sqlite.save(["date", "title"], event)

    # In theory at this point we would find the "next page" link and then
    # scrape the rest of the events, but it uses some nasty-looking JS.

scrape_page("http://www.theberrytheatre.co.uk/whats%20on.aspx?category=all")