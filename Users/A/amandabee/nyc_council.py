import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://council.nyc.gov/html/members/members.shtml")
raw = lxml.html.fromstring(html)

for tr in raw.cssselect("table#members_table"):
    print tr.text_content();
    print tr[1].tag
    print tr[0].tag
#    print eg[1].getparent().tag    # table
#    print eg[1].getprevious().tag  # tr
    print tr[1].getnext().text_content()          #Charles Barron
#    print eg[1].getchildren().tag     # [<Element em>]
    eglist = tr[1].getchildren()
    for gp in list(eglist):
        record = { "gp" : gp.text } # create a column name and store the text of each occurrencef


#for table in raw.cssselect("table.sortable"):
#        tds = table.cssselect("td");
#        data = {
#            'member' : tds[1].text_content(),
#            'district' : tds[2].text_content(),
#            'boro' : tds[3].text_content(),
#            'party' : tds[4].text_content()
#        }
#
#        print data
#        scraperwiki.sqlite.save(unique_keys=['member'], data=data)



import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://council.nyc.gov/html/members/members.shtml")
raw = lxml.html.fromstring(html)

for tr in raw.cssselect("table#members_table"):
    print tr.text_content();
    print tr[1].tag
    print tr[0].tag
#    print eg[1].getparent().tag    # table
#    print eg[1].getprevious().tag  # tr
    print tr[1].getnext().text_content()          #Charles Barron
#    print eg[1].getchildren().tag     # [<Element em>]
    eglist = tr[1].getchildren()
    for gp in list(eglist):
        record = { "gp" : gp.text } # create a column name and store the text of each occurrencef


#for table in raw.cssselect("table.sortable"):
#        tds = table.cssselect("td");
#        data = {
#            'member' : tds[1].text_content(),
#            'district' : tds[2].text_content(),
#            'boro' : tds[3].text_content(),
#            'party' : tds[4].text_content()
#        }
#
#        print data
#        scraperwiki.sqlite.save(unique_keys=['member'], data=data)



