import scraperwiki
import lxml.html
import re

from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc)

url = "http://socialcompare.com/en/comparison/popular-upcoming-2011-tablets"
#html = scraperwiki.scrape("http://socialcompare.com/en/comparison/tasks-management-todo-lists-web-apps")
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)

table =  root.cssselect("table[class='s-t']")[0]

rawitems = table.cssselect("th.item")

items = []
i = 0
for item in rawitems:
    name = item.text_content().strip()
    items.append({'key': name+str(i)})
    i += 1

def get_cell_value(elem):
    text = elem.text_content()
    yes = elem.find_class('scYes')
    no = elem.find_class('scNo')
    maybe = elem.find_class('scMaybe')
    if len(yes) > 0:
        return "YES; " + yes[0].text_content() 
    if len(no) > 0:
        return "NO; " + no[0].text_content() 
    if len(maybe) > 0:
        return "MAYBE; " + maybe[0].text_content() 
    return text



rows = table.cssselect("tbody > tr")

for row in rows:
    th = row.cssselect("th")[0]
    rowname = th.text_content().strip()
    if rowname != "":
        rowname = re.sub(r'[ -/\xa0\xae]+','_',rowname)
        value_items = row.cssselect("td")
        if len(value_items) > 0:
            for i in xrange(len(items)):
                item = items[i]
                item[rowname] = get_cell_value(value_items[i])

print items
scraperwiki.sqlite.save(unique_keys=["key"], data=items)
import scraperwiki
import lxml.html
import re

from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc)

url = "http://socialcompare.com/en/comparison/popular-upcoming-2011-tablets"
#html = scraperwiki.scrape("http://socialcompare.com/en/comparison/tasks-management-todo-lists-web-apps")
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)

table =  root.cssselect("table[class='s-t']")[0]

rawitems = table.cssselect("th.item")

items = []
i = 0
for item in rawitems:
    name = item.text_content().strip()
    items.append({'key': name+str(i)})
    i += 1

def get_cell_value(elem):
    text = elem.text_content()
    yes = elem.find_class('scYes')
    no = elem.find_class('scNo')
    maybe = elem.find_class('scMaybe')
    if len(yes) > 0:
        return "YES; " + yes[0].text_content() 
    if len(no) > 0:
        return "NO; " + no[0].text_content() 
    if len(maybe) > 0:
        return "MAYBE; " + maybe[0].text_content() 
    return text



rows = table.cssselect("tbody > tr")

for row in rows:
    th = row.cssselect("th")[0]
    rowname = th.text_content().strip()
    if rowname != "":
        rowname = re.sub(r'[ -/\xa0\xae]+','_',rowname)
        value_items = row.cssselect("td")
        if len(value_items) > 0:
            for i in xrange(len(items)):
                item = items[i]
                item[rowname] = get_cell_value(value_items[i])

print items
scraperwiki.sqlite.save(unique_keys=["key"], data=items)
