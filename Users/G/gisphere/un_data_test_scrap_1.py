import scraperwiki
html = scraperwiki.scrape("http://www.sahibinden.com/search.php?&b[special_type]=last48&b[sort_field]=date_first_activated2&b[sort_order]=asc&b[page]=1")
print html

import lxml.html
root = lxml.html.fromstring(html)
tds = root.cssselect('table#table_main_list') # get all the <td> tags
for td in tds:
    data = {
      'title' : td.text_content(),
  #     'price' : tds[1].text_content(),
  #     'men' : tds[7].text_content(),
   #    'women' : tds[9].text_content(),
 #      'total' : int(tds[4].text_content())
    }
    print data

for td in tds:
    record = { "td" : td.text_content } # column name and value
scraperwiki.sqlite.save(["td"], record) # save the records one by one
