#There's no RSS feed for Private Eye covers, so I'll make my own...
import scraperwiki
import lxml.html
issue = 1
url = "http://www.private-eye.co.uk/covers.php?showme="
html = scraperwiki.scrape(url + str(issue))
root = lxml.html.fromstring(html)


def get_issue_info():
    html = scraperwiki.scrape(url + str(issue))
    root = lxml.html.fromstring(html)
    date = root.cssselect("div.content span")[1]
    coverstarstext = root.cssselect("div.content td.text a.blog_smaller")
    coverstars = []
    for each in coverstarstext:
        if each.text is not None:
            if "Issue" not in each.text and each.text is not None:
                coverstars.append(each.text)
    print date.text
    if coverstars == []:
        coverstars = ""
    print coverstars
    scraperwiki.sqlite.save(unique_keys=["issue"], data={"issue":issue,"date":date.text, "coverstars":coverstars})

for each in range(1236,1312):
    if len(root.cssselect("div.content span")) > 0:
        issue = each
        get_issue_info()


#There's no RSS feed for Private Eye covers, so I'll make my own...
import scraperwiki
import lxml.html
issue = 1
url = "http://www.private-eye.co.uk/covers.php?showme="
html = scraperwiki.scrape(url + str(issue))
root = lxml.html.fromstring(html)


def get_issue_info():
    html = scraperwiki.scrape(url + str(issue))
    root = lxml.html.fromstring(html)
    date = root.cssselect("div.content span")[1]
    coverstarstext = root.cssselect("div.content td.text a.blog_smaller")
    coverstars = []
    for each in coverstarstext:
        if each.text is not None:
            if "Issue" not in each.text and each.text is not None:
                coverstars.append(each.text)
    print date.text
    if coverstars == []:
        coverstars = ""
    print coverstars
    scraperwiki.sqlite.save(unique_keys=["issue"], data={"issue":issue,"date":date.text, "coverstars":coverstars})

for each in range(1236,1312):
    if len(root.cssselect("div.content span")) > 0:
        issue = each
        get_issue_info()


