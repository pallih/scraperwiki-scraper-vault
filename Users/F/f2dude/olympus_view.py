import scraperwiki
import ast

sourceScraper = "olympus-fourthirds"

## assign to scraper of D1
scraperwiki.sqlite.attach(sourceScraper)

data = scraperwiki.sqlite.select(
    '''* from swdata'''
)
print "<table>"

## create list with keys we want to show in table
keys = data[0].keys()
keys.remove("title")
keys.remove("href")
keys.remove("Menu")
print "<tr>"
print "<th>Model</th>"

## helpers to print TD and TH html elements
def printHead(x): print '<th>%s</th>' % x
def printCell(x): print '<td>%s</td>' % x

## print THs (column-headings)
map(printHead, keys)

print "</tr>"
for d in data:
    print "<tr>"
    printHead(d["title"])
    ## iterate over data and put each in as TD
    for key in keys:
        if d[key]:
            component = ast.literal_eval(d[key])
            for k, v in component.iteritems():
                tdcontent = '<dt>%s</dt><dd>%s</dd>' % (k, v)
            printCell("<dl>" + tdcontent + "</dl>")
        else:
            printCell("&nbsp;")
    print "</tr>"

print "</table>"

import scraperwiki
import ast

sourceScraper = "olympus-fourthirds"

## assign to scraper of D1
scraperwiki.sqlite.attach(sourceScraper)

data = scraperwiki.sqlite.select(
    '''* from swdata'''
)
print "<table>"

## create list with keys we want to show in table
keys = data[0].keys()
keys.remove("title")
keys.remove("href")
keys.remove("Menu")
print "<tr>"
print "<th>Model</th>"

## helpers to print TD and TH html elements
def printHead(x): print '<th>%s</th>' % x
def printCell(x): print '<td>%s</td>' % x

## print THs (column-headings)
map(printHead, keys)

print "</tr>"
for d in data:
    print "<tr>"
    printHead(d["title"])
    ## iterate over data and put each in as TD
    for key in keys:
        if d[key]:
            component = ast.literal_eval(d[key])
            for k, v in component.iteritems():
                tdcontent = '<dt>%s</dt><dd>%s</dd>' % (k, v)
            printCell("<dl>" + tdcontent + "</dl>")
        else:
            printCell("&nbsp;")
    print "</tr>"

print "</table>"

