#There's no RSS feed for Private Eye covers, so I'll make my own...

#Still need to write code to get most recent issue number from datastore and try the next one
import scraperwiki
import lxml.html
issue = 1239
url = "http://www.private-eye.co.uk/covers.php?showme="
html = scraperwiki.scrape(url + str(issue))
root = lxml.html.fromstring(html)


def get_issue_info():
    html = scraperwiki.scrape(url + str(issue))
    root = lxml.html.fromstring(html)
    if len(root.cssselect("div.content span")) > 0:
        date = root.cssselect("div.content span")[1].text
    else:
        date = ""
    coverstarstext = root.cssselect("div.content td.text a.blog_smaller")
    coverstars = []
    for each in coverstarstext:
        if each.text is not None:
            if "Issue" not in each.text and each.text is not None:
                coverstars.append(each.text)
    print date
    if coverstars == []:
        coverstars = ""
    print coverstars
    scraperwiki.sqlite.save(unique_keys=["issue"], data={"issue":issue,"date":date, "coverstars":coverstars})

while len(root.cssselect("div.content span")) > 0:
        issue = issue + 1
        get_issue_info()
        html = scraperwiki.scrape(url + str(issue))
        root = lxml.html.fromstring(html)
        



