import scraperwiki
import lxml.html

it_html = scraperwiki.scrape("http://indigenoustweets.com/")

print it_html

root = lxml.html.fromstring(it_html)

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds) == 6:
        data = { "language": tds[0].text_content(),
                "users": int(tds[1].text_content()),
                "tweets": int(tds[2].text_content()),
                "top user": tds[3].text_content(),
                "top user tweets": int(tds[4].text_content()),
                "first tweet": tds[5].text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=["language"], data=data)
