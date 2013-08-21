# import scraperwiki           
# import lxml.html

# html = scraperwiki.scrape('http://ciwqs.waterboards.ca.gov/ciwqs/ewrims/EWServlet?Page_From=EWWaterRightPublicSearch.jsp&Redirect_Page=EWWaterRightPublicSearchResults.jsp&Object_Expected=EwrimsSearchResult&Object_Created=EwrimsSearch&Object_Criteria=&Purpose=&appNumber=&permitNumber=&licenseNumber=&watershed=&countyTypeIDs=1&waterHolderName=&source=')
# root = lxml.html.fromstring(html)

# for el in root.cssselect("table.dataentry tr"):           
#     print el
#     print lxml.html.tostring(el)



import scraperwiki
html = scraperwiki.scrape('http://ciwqs.waterboards.ca.gov/ciwqs/ewrims/EWServlet?Page_From=EWWaterRightPublicSearch.jsp&Redirect_Page=EWWaterRightPublicSearchResults.jsp&Object_Expected=EwrimsSearchResult&Object_Created=EwrimsSearch&Object_Criteria=&Purpose=&appNumber=&permitNumber=&licenseNumber=&watershed=&countyTypeIDs=1&waterHolderName=&source=')
print "Click on the ...more link to see the whole page"
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('form>table>table>table.dataentry tbody tr td') # get all the <td> tags

for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag

for td in tds:
     record = { "td" : td.text } # column name and value
     scraperwiki.sqlite.save(["td"], record) # save the records one by one