import scraperwiki
html = scraperwiki.scrape('https://scraperwiki.com/hello_world.html')
print html

#import lxml.html           
#root = lxml.html.fromstring(html)
#tds = root.cssselect('div') # get all the <td> tags
#for td in tds:
#    print lxml.html.tostring(td) # the full HTML tag
#    print td.text                # just the text inside the HTML tag
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)

