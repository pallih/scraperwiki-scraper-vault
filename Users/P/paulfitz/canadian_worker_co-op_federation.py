import scraperwiki           
html = scraperwiki.scrape("http://www.canadianworker.coop/basics/members")

def get_part(entry,name):
    try:
        return entry.cssselect("div.views-field-" + name)[0].cssselect("span.field-content")[0].text_content()
    except:
        return entry.cssselect("div.views-field-" + name)[0].cssselect("div.field-content")[0].text_content()

import lxml.html           
root = lxml.html.fromstring(html)
category = ""

for entry in root.cssselect("div.views-row,h1"):
    try:
        data = {
          'title' : get_part(entry,"title"),
          'category': category,
          'street' : get_part(entry,"street"),
          'city' : get_part(entry,"city"),
          'province' : get_part(entry,"province"),
          'email' : get_part(entry,"field-email-email"),
          'website' : get_part(entry,"field-website-url"),
          'description' : get_part(entry,"body"),
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
    except:
        category = entry.text_content()
        print category

# Hack to update view
scraperwiki.sqlite.commit
scraperwiki.scrape("https://views.scraperwiki.com/run/cwcf_changes/?")
import scraperwiki           
html = scraperwiki.scrape("http://www.canadianworker.coop/basics/members")

def get_part(entry,name):
    try:
        return entry.cssselect("div.views-field-" + name)[0].cssselect("span.field-content")[0].text_content()
    except:
        return entry.cssselect("div.views-field-" + name)[0].cssselect("div.field-content")[0].text_content()

import lxml.html           
root = lxml.html.fromstring(html)
category = ""

for entry in root.cssselect("div.views-row,h1"):
    try:
        data = {
          'title' : get_part(entry,"title"),
          'category': category,
          'street' : get_part(entry,"street"),
          'city' : get_part(entry,"city"),
          'province' : get_part(entry,"province"),
          'email' : get_part(entry,"field-email-email"),
          'website' : get_part(entry,"field-website-url"),
          'description' : get_part(entry,"body"),
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)
    except:
        category = entry.text_content()
        print category

# Hack to update view
scraperwiki.sqlite.commit
scraperwiki.scrape("https://views.scraperwiki.com/run/cwcf_changes/?")
