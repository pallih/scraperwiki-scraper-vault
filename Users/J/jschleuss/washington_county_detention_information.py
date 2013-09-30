import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.co.washington.ar.us/sheriff/resource/DintakeRoster.asp")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    # if td count is 8 and the first td is not 'Name Last, First Middle'
    if len(tds)==8 and not str(tds[0].text_content())=="Name Last, First Middle":
        data = {
            #incoming_data = [item.split(",")[1] for item in stream if item]
            #'name' : tds[0].text_content[0],

            'name_first' : tds[0].text_content().split(" ,")[-1],
            'name_last' : tds[0].text_content().split(" , ")[0],
            'age' : tds[1].text_content(),
            'race' : tds[2].text_content(),
            'sex' : tds[3].text_content(),
            'book_date' : tds[4].text_content(),
            'book_time' : tds[5].text_content(),
            'release_date' : tds[6].text_content(),
            'release_time' : tds[7].text_content()
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
import scraperwiki

# Blank Python

import scraperwiki
html = scraperwiki.scrape("http://www.co.washington.ar.us/sheriff/resource/DintakeRoster.asp")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    # if td count is 8 and the first td is not 'Name Last, First Middle'
    if len(tds)==8 and not str(tds[0].text_content())=="Name Last, First Middle":
        data = {
            #incoming_data = [item.split(",")[1] for item in stream if item]
            #'name' : tds[0].text_content[0],

            'name_first' : tds[0].text_content().split(" ,")[-1],
            'name_last' : tds[0].text_content().split(" , ")[0],
            'age' : tds[1].text_content(),
            'race' : tds[2].text_content(),
            'sex' : tds[3].text_content(),
            'book_date' : tds[4].text_content(),
            'book_time' : tds[5].text_content(),
            'release_date' : tds[6].text_content(),
            'release_time' : tds[7].text_content()
        }
        print data

        scraperwiki.sqlite.save(unique_keys=['name_first'], data=data)
