# See https://scraperwiki.com/docs/python/python_intro_tutorial/

# 1. Create a new scraper, choose Python (Ruby or PHP) as the language.
# Use any normal Python library to crawl the web, such as urllib2 or Mechanize. 
# There is also a simple built in ScraperWiki library which may be easier

import scraperwiki

# Blank Python

# 2. Download HTML from the web, click the “Run” button or type Ctrl+R.

html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html

# See any output you printed in the Console tab
# When it is something quite large, click "more" in the console to view it all. 
# Or, use the Sources tab in the editor to see everything that has been downloaded.

# 3. Parsing the HTML to get your content
# lxml is the best library for extracting content from HTML.

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        # print data
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

# Code like 'div' and 'td' are CSS selectors, like those used to style HTML. 
# They are to select all the table rows, 
    # then for each of those rows select the individual cells, 
    # and if there are 12 of them (ie: the main table body, not header rows), 
    # extract the country name and schooling statistic.

# 4. Saving to the ScraperWiki datastore
# The datastore is a magic SQL store, one where you don't need to make a schema up front.
# Replace print data in the lxml loop with this save command

#         scraperwiki.sqlite.save(unique_keys=['country'], data=data)

# The unique keys (just country in this case) identify each piece of data. 
# When the scraper runs again, existing data with the same values for the unique keys is replaced.
# Go to the Data tab in the editor to see the data loading in.

# 5. Getting the data out again ... 
# press "save scraper" at the bottom right of the editor, give your scraper a title.

# click on thDocumentatione Scraper tab at the top right to see a preview of your data.
# The easiest way to get it all out is to "Download spreadsheet (CSV)".

# For more complex queries "Explore with ScraperWiki API". Try this query in the SQL query box:

# select * from swdata order by years_in_school desc limit 10

# It gives the 10 countries where children spend the most years at school, in descending order.
# As well as JSON, you can also get custom CSV files using the SQL query in the URL.

# Next?
# Start writing or take a look at the documentation:
# https://scraperwiki.com/docs/python/