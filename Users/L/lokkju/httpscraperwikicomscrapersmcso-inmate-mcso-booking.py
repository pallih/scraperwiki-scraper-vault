# Blank Python
sourcescraper = 'mcso_inmate_booking_data_parse'
import scraperwiki
import os
import json
import sys
import urllib

scraperwiki.sqlite.attach("mcso_inmate_booking_data_parse", "src")
base_url = "http://www.mcso.us/PAID/"
limit = 40
offset = 0
i = 0
results = scraperwiki.sqlite.select(
    "d.booking_id,p.name FROM booking_detail d LEFT JOIN person p ON p.booking_id=d.booking_id ORDER BY d.booking_date DESC LIMIT ?,?",(offset,limit))
for rdata in results:
    img_url = "%sImageHandler.axd?mid=%s&size=F" % (base_url,urllib.quote_plus(rdata["booking_id"]))
    booking_url = "%sBookingDetail.aspx?ID=%s" % (base_url,urllib.quote_plus(rdata["booking_id"]))
    name = rdata["name"]
    
    print '<a href="%s" target="_blank" title="%s"><img src="%s" alt="%s" width="240" height="300" onerror="this.onerror=null;this.src=%s"/></a>' % (booking_url,name,img_url,name,"'http://www.mcso.us/PAID/images/no_photo.jpg'")
    i = i + 1
    if(i % 4 == 0):
        print '<br/>'
    if i == limit:
        break
    
    
