import scraperwiki
import datetime

 
scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")


def results():
    return scraperwiki.sqlite.select("`Local authority`,`Project description`,`Grant amount`,`link`,`Grant date`,`Distributing body`,`Recipient` FROM uk_lottery_scrapedownload_1.swdata WHERE (`Grant date` > date('now','-1 year')) AND (`Local authority` = 'Liverpool' OR `Local authority` = 'Knowsley' OR `Local authority` = 'Sefton' OR `Local authority` = 'St. Helens' OR `Local authority` = 'Wirral') ORDER BY `Grant date` DESC")



def header(r):
    s = u""
    s += "<tr>"
    for x in r:
        s += "<th>"
        s += unicode(x)
        s += "</th>"
    s += "</tr>"
    return s
 

def colour(n):
    if n == u'Liverpool':
        return "#ff37f8"
    elif n == u'Knowsley':
        return "#ff0e36"
    elif n == u'St. Helens':
        return "#ff9711"
    elif n == u'Wirral':
        return "#44ff25"
    elif n == u'Sefton':
        return "#fcff25"
    else:
        raise "Shouldn't happen"


def datarow(r):
    s = u""
    s += '<tr style="background-color:%s">'%colour(r[0])
    for x in r:
        s += "<td>"
        s += unicode(x)
        s += "</td>"
    s += "</tr>"
    return s


def table(a):
    s = u""
    s += "<table>"
    s += header(a[0])
    for r in a[1:]:
        s += datarow(r)
    s += "</table>"
    return s
 

def main():
    h = ["Local authority","Recipient","Description","Amount","Link","Grant date","Distributing body"]
    t = [h]+list([d["Local authority"],d["Recipient"],d["Project description"],d["Grant amount"],'<a href="%s">link</a>'%d["link"],d["Grant date"],d["Distributing body"]] for d in results())
    print "<br />"*4 + table(t)


main()
