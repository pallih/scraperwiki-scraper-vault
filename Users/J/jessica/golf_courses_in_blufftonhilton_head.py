import scraperwiki
import lxml.html
from lxml.cssselect import CSSSelector

html = scraperwiki.scrape("http://www.golflink.com/golf-courses/searchresults.aspx?coursekeyword=&coursecity=&coursestate=&coursename=&coursezip=29910&within=20")

root = lxml.html.fromstring(html)
result = root.cssselect(".search_result")

for div in result:
    title = div.cssselect('.title')[0].cssselect('a')[0].text_content()
    club = title.partition(',')[0]
    course = title.partition(',')[2]
    des = div.cssselect('.content')[0].cssselect('p')[0].text_content()
    try:
        address = des.replace("\n\t\t\t\t\t\t\r","||").split("||")[4]
    except IndexError:
        print "error"
    try:
        access = des.replace("\n\t\t\t\t\t\t\r","||").split("||")[3].replace("(","").replace(")","")
    except IndexError:
        print "error"
    data = {
        'club': club,
        'course': course,
        'des': des,
        'address': address,
        'access' : access
    }
    scraperwiki.sqlite.save( unique_keys=['club'], data=data)
    #print addressimport scraperwiki
import lxml.html
from lxml.cssselect import CSSSelector

html = scraperwiki.scrape("http://www.golflink.com/golf-courses/searchresults.aspx?coursekeyword=&coursecity=&coursestate=&coursename=&coursezip=29910&within=20")

root = lxml.html.fromstring(html)
result = root.cssselect(".search_result")

for div in result:
    title = div.cssselect('.title')[0].cssselect('a')[0].text_content()
    club = title.partition(',')[0]
    course = title.partition(',')[2]
    des = div.cssselect('.content')[0].cssselect('p')[0].text_content()
    try:
        address = des.replace("\n\t\t\t\t\t\t\r","||").split("||")[4]
    except IndexError:
        print "error"
    try:
        access = des.replace("\n\t\t\t\t\t\t\r","||").split("||")[3].replace("(","").replace(")","")
    except IndexError:
        print "error"
    data = {
        'club': club,
        'course': course,
        'des': des,
        'address': address,
        'access' : access
    }
    scraperwiki.sqlite.save( unique_keys=['club'], data=data)
    #print address