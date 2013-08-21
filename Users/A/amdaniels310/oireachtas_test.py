import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.oireachtas.ie/members-hist/default.asp?housetype=1&HouseNum=24&disp=mem")
root = lxml.html.fromstring(html)
for el in root.cssselect("#memberslist b"):
    mem = el.text
    print el
    print el.text
    if mem is not None:
        data = {
            'Member Name' : mem,
          }
        print data
        scraperwiki.sqlite.save(unique_keys=['Member Name'], data=data)



