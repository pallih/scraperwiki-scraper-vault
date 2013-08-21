import scraperwiki

# Blank Python
#html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")


#bigurl = scraperwiki.scrape(http://www.meganslaw.ca.gov/cgi/prosoma.dll?zoomAction=Box&zoomAction=clickcenter&zoomAction=clickoffender&lastName=&firstName=&Address=&City=&zipcode=&searchDistance=.75&City2=&countyLocation=&zipcode2=&SelectCounty=SACRAMENTO&ParkName=&searchDistance2=.75&City3=&zipcode3=&countyLocation3=&schoolName=&searchDistance3=.75&City4=&zipcode4=&countyLocation4=&refineID=&pan=&distacross=107211&centerlat=38409907&centerlon=-121514242&starlat=&starlon=&startext=&x1=&y1=&x2=&y2=&mapwidth=525&mapheight=400&zoom=&searchBy=countylist&id=&docountycitylist=2&OFDTYPE=&W6=178345%0D%0A&lang=ENGLISH&W6=178345)

#this code requires a session identifier (6=xxxxxx), so you need to hit meganslaw first and grab one
county = 'SACRAMENTO'
a = 0
while a < 1:
    a = a+1
    core = 'http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6=766238&searchby=CountyList&SelectCounty='+ county +'&SB=0&PageNo='+ str(a)
    html = scraperwiki.scrape(core)
#    print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("SPLIT"): #pretty sure I'm not using this command correctly
    tds = tr.cssselect("td")
    if len(tds)==7:
        data = {
            'soffender' : tds[0].text_content(),
            'second' : tds[1].text_content()
        }
        print data
        #scraperwiki.sqlite.save(unique_keys=['soffender'], data=data)

#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        scraperwiki.sqlite.save(unique_keys=['country'], data=data)




