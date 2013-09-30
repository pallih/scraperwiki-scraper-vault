import scraperwiki


scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")
scraperwiki.sqlite.attach("uk_population_by_local_authority_2008")


def shortform(n):
    return n.replace(" ","").replace("-","").replace(".","").lower()


def comparison_form(d):
    return dict((shortform(k),(k,v)) for (k,v) in d.iteritems())


def reconcile(d1,d2):
    d1s = comparison_form(d1)
    d2s = comparison_form(d2)

    for (k,(n2,v2)) in d2s.iteritems():
        if k in d1s:
            (n1,v1) = d1s[k]
            yield (n2,v1,v2)


def amounts():
    return dict((d[u'Local authority'],d[u'grantamount']) for d in scraperwiki.sqlite.select('`Local authority`, SUM(`Grant amount`) as grantamount FROM uk_lottery_scrapedownload_1.swdata GROUP BY `Local authority`'))


def populations():
    return dict((d[u'name'],d[u'population']) for d in scraperwiki.sqlite.select('`name`,`population` FROM uk_population_by_local_authority_2008.swdata'))


def amounts_per_person():
    l = list((place,pop,amount,amount*1.0/pop) for (place,pop,amount) in reconcile(populations(),amounts()))
    l.sort(key = (lambda x: x[3]))
    return l


def header(r):
    s = ""
    s += "<tr>"
    for x in r:
        s += "<th>"
        s += str(x)
        s += "</th>"
    s += "</tr>"
    return s


def datarow(r):
    s = ""
    s += "<tr>"
    for x in r:
        s += "<td>"
        s += str(x)
        s += "</td>"
    s += "</tr>"
    return s


def table(a):
    s = ""
    s += "<table>"
    s += header(a[0])
    for r in a[1:]:
        s += datarow(r)
    s += "</table>"
    return s


def main():
    print table([["Local authority","Population in 2008","Lottery funding","Funding per capita"]]+amounts_per_person())



main()
import scraperwiki


scraperwiki.sqlite.attach("uk_lottery_scrapedownload_1")
scraperwiki.sqlite.attach("uk_population_by_local_authority_2008")


def shortform(n):
    return n.replace(" ","").replace("-","").replace(".","").lower()


def comparison_form(d):
    return dict((shortform(k),(k,v)) for (k,v) in d.iteritems())


def reconcile(d1,d2):
    d1s = comparison_form(d1)
    d2s = comparison_form(d2)

    for (k,(n2,v2)) in d2s.iteritems():
        if k in d1s:
            (n1,v1) = d1s[k]
            yield (n2,v1,v2)


def amounts():
    return dict((d[u'Local authority'],d[u'grantamount']) for d in scraperwiki.sqlite.select('`Local authority`, SUM(`Grant amount`) as grantamount FROM uk_lottery_scrapedownload_1.swdata GROUP BY `Local authority`'))


def populations():
    return dict((d[u'name'],d[u'population']) for d in scraperwiki.sqlite.select('`name`,`population` FROM uk_population_by_local_authority_2008.swdata'))


def amounts_per_person():
    l = list((place,pop,amount,amount*1.0/pop) for (place,pop,amount) in reconcile(populations(),amounts()))
    l.sort(key = (lambda x: x[3]))
    return l


def header(r):
    s = ""
    s += "<tr>"
    for x in r:
        s += "<th>"
        s += str(x)
        s += "</th>"
    s += "</tr>"
    return s


def datarow(r):
    s = ""
    s += "<tr>"
    for x in r:
        s += "<td>"
        s += str(x)
        s += "</td>"
    s += "</tr>"
    return s


def table(a):
    s = ""
    s += "<table>"
    s += header(a[0])
    for r in a[1:]:
        s += datarow(r)
    s += "</table>"
    return s


def main():
    print table([["Local authority","Population in 2008","Lottery funding","Funding per capita"]]+amounts_per_person())



main()
