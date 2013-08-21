import scraperwiki

# the above line loads the python library to scrape it is similar to
# beautiful soup http://www.crummy.com/software/BeautifulSoup/ or cURL

# the  line below calls the scrape proceedure of the scraperwiki library (group of functions)
# and puts  the in the contents (a long string of html - the whole page) in the variable html

html = scraperwiki.scrape("http://benbow.site40.net/hdlibraries/samp.html")
print html

import lxml.html
root = lxml.html.fromstring(html)

# the above line loads the captured html into an xml DOM object arbitrarilly called 'root'

# root is the DOM object loaded above
# the following 3 lines say "for each <tr> in the in the captured html in 'root' select all of the <td>s
# if there are 9 <td>s (i know the table i want has 9 columns) then grab the td data
# the gabbed data is put in the array tds[0] holds 'name' and tds[1] holds 'location ... from the table  

for tr in root.cssselect("tr"):
    tds = tr.cssselect("td")
    if len(tds)==9: 
        data = {
             'name' : tds[0].text_content(),
             'location' : tds[1].text_content(),
             'owner' : tds[3].text_content(),
             'color' : tds[2].text_content(),
             'age' : tds[4].text_content(),
             'builder' : tds[5].text_content(),
             'engine' : tds[6].text_content(),
             'layout' : tds[7].text_content(),
             'remarks' : tds[8].text_content()
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)

# the above line saves the nine pieces of data to the database 
# there are about 30 rows <tr>s in the samphire registry page so for each of those rows
# nine pieces of data will be written to a corresponding row in the database
 
