import scraperwiki
from datetime import datetime
html = scraperwiki.scrape('http://www.ewrc-results.com/final.php?e=11092&t=Mourne-Rally-2013')
#print html


import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
trs = root.cssselect('tr') # get all the <tr> tags
rowCounter = 0
for tr in trs:
    # Normally results are length 10
    if (len(tr) == 10):
        #Used to help me understand the size of various rows
        rowCounter += 1
        #print "Row " + str(rowCounter) + " has " + str(len(tr)) + " elements."

        if rowCounter != 1:
            #Extract indicies used to idenitify driver names
            driverXMLStr = lxml.html.tostring(tr[3])
            namesStart = driverXMLStr.find("> ")
            namesMiddle = driverXMLStr.find(" - ") 
            namesEnd = driverXMLStr.find("</a")
            timeData = datetime.strptime(tr[7].text,"%H:%M:%S.%f")
            
            #print driverXMLStr[namesStart+2:namesMiddle]
            #print driverXMLStr[namesMiddle+3:namesEnd]
            #print lxml.html.tostring(tr[3])
            #print float((timeData.microsecond / 1000000))
        
            # Extract the data from each row
            extractedData = {
                                "CarNumber": int(tr[1].text[1:len(tr[1].text)]),
                                "DriverName": driverXMLStr[namesStart+2:namesMiddle],
                                "CoDriverName": driverXMLStr[namesMiddle+3:namesEnd],
                                "CarType": tr[5].text,
                                "GroupType": int(tr[6].text),
                                "TimeString": tr[7].text,                                
                                "Time": timeData,
                                "TimeInSeconds": float((timeData.microsecond / 1000000)) + timeData.second + (timeData.minute * 60) + (timeData.hour * 3600)
                            }
            #print extractedData
        
            # Not going to save the column row
            #print "Save row: " + str(rowCounter)
            scraperwiki.sqlite.save(unique_keys=['CarNumber'],data=extractedData)
    
        # Code to print various row data
        if False:
            manDx = 0
            for td in tr:
                print "Counter: " + str(manDx)
                print "Length: " + str(len(td))
                print "Tag: " + td.tag
                print lxml.html.tostring(td) # the full HTML tag
                print td.text                # just the text inside the HTML tag
                manDx += 1
    



#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one


