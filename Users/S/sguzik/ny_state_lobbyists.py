import scraperwiki
import lxml.html

scraperwiki.sqlite.attach("ny_state_lobby")
lhtml = scraperwiki.sqlite.execute("select html2 from indivlobb")["data"]
for html0 in lhtml:
    print html0[0]

    root = lxml.html.fromstring(html0[0])
    for row in root.cssselect("table#LobbyistInfo_GLobbyInfo tr"):
        print [ td.text_content().strip()  for td in row ]
    print "------"

    tab1 = root.cssselect("td#ClientInfo_tdVClientName")[0].getparent().getparent()
    for row in tab1.cssselect("tr"):
        print [ td.text_content().strip()  for td in row ]
    print "------"

    for t in root.cssselect("table"):
        print lxml.html.tostring(t)
    break
import scraperwiki
import lxml.html

scraperwiki.sqlite.attach("ny_state_lobby")
lhtml = scraperwiki.sqlite.execute("select html2 from indivlobb")["data"]
for html0 in lhtml:
    print html0[0]

    root = lxml.html.fromstring(html0[0])
    for row in root.cssselect("table#LobbyistInfo_GLobbyInfo tr"):
        print [ td.text_content().strip()  for td in row ]
    print "------"

    tab1 = root.cssselect("td#ClientInfo_tdVClientName")[0].getparent().getparent()
    for row in tab1.cssselect("tr"):
        print [ td.text_content().strip()  for td in row ]
    print "------"

    for t in root.cssselect("table"):
        print lxml.html.tostring(t)
    break
