import scraperwiki
import re
import urllib
import urllib2
import simplejson as json
from types import *
from datetime import date, timedelta, datetime


# positiveNumber = ahead of sked, negativeNumber = behind sked
def calculateDelay(date1, date2):
    d1 = datetime.strptime(date1[:10], "%Y-%m-%d")
    d2 = datetime.strptime(date2[:10], "%Y-%m-%d")
    return (d1 - d2).days

def printOverdueResults():
    result = scraperwiki.sqlite.execute("SELECT serviceRequestID, address, delay, estimatedResponse FROM graffiti WHERE status = 'closed' AND delay < 0 order by updatedDate desc, delay asc, estimatedResponse desc")
    print "********* OVERDUE REQUESTS *********"
    for each in result["data"]:
         print 'ID: ' + str(each[0]) + ', created: ' + str(each[1]) + ', delay: '+ str(each[2]) + ', estimatedResponse:' + str(each[3])
    print "************************************"

def printOverdueResults2():
    result = scraperwiki.sqlite.execute("SELECT requestDate, expectedDate, updatedDate FROM graffiti WHERE status = 'closed' order by updatedDate desc, delay asc, estimatedResponse desc")
    print "********* OVERDUE REQUESTS *********"
    for each in result["data"]:
         print 'created: ' + str(each[0]) + ' , estimate: ' + str(each[1]) + ' , finished: ' + str(each[2]) 

    print "************************************"

def commentsChecker(requestIDs):

        for each in requestIDs["data"]: 
                requestID = each[0]
                result = scraperwiki.sqlite.execute("SELECT status, expectedDate, updatedDate FROM graffiti_temp WHERE serviceRequestID = ?",(requestID))
                     
                if each[1] != result["data"][0][0]:
                    print "STATUS HAS CHANGED!"
                    # find diff between estimated date (i.e. fixed) and updated date to find difference
                    delay = calculateDelay(each[3], result["data"][0][2])

                    scraperwiki.sqlite.execute("UPDATE graffiti SET status = 'closed', updatedDate = ?, delay = ? WHERE serviceRequestID = ?",(result["data"][0][2], delay, requestID))
                    scraperwiki.sqlite.commit() 
                else:
                    print "REQUEST UNCHANGED."
                    pass

# Defines the function that processes the text using regular expressions and pulls out what we need, send it to the update
def commentsUpdate(ID, serviceName, status, notes, requested_datetime, updated_datetime, expected_datetime, address, longCoord, latCoord, media):

        result = scraperwiki.sqlite.execute("SELECT count(*) FROM graffiti WHERE serviceRequestID = ?", (ID))
        test = result["data"]

        # this checks result in 'data' array
        if test[0][0] == 0:
                print "New 311 Request. Adding to database."
                if expected_datetime is None:
                    estimatedResponseDays = 0
                else:
                    estimatedResponseDays = calculateDelay(requested_datetime, expected_datetime)
                scraperwiki.sqlite.execute("insert into graffiti values (?,?,?,?,?,?,?,?,?,?,?,?,?)", (ID, serviceName, status, notes, requested_datetime, expected_datetime, updated_datetime, address, longCoord, latCoord, media, estimatedResponseDays,"0"))
                scraperwiki.sqlite.execute("insert into graffiti_temp values (?,?,?,?,?,?,?,?,?,?,?)", (ID, serviceName, status, notes, requested_datetime, expected_datetime, updated_datetime, address, longCoord, latCoord, media))
                scraperwiki.sqlite.commit()
                # Map request here!
                # Tweet here?

        else:
                print "311 Request exists."
                scraperwiki.sqlite.execute("insert into graffiti_temp values (?,?,?,?,?,?,?,?,?,?,?)", (ID, serviceName, status, notes, requested_datetime, updated_datetime, expected_datetime, address, longCoord, latCoord, media))
                scraperwiki.sqlite.commit() 

def idGetter():

        scraperwiki.sqlite.execute("DELETE FROM graffiti_temp")
       
        todayDate = str(date.today() + timedelta(days=1))
        searchDate = str(date.today() - timedelta(days=31))

        url = "https://secure.toronto.ca/webwizard/ws/requests.json?start_date=" + searchDate + "&end_date=" + todayDate + "&service_code=CSROWC-05,CSROWBM-03,%20CSROSC-14,30102,SWLMALB-02&jurisdiction_id=toronto.ca"

        #url = "http://www.marcellison.com/json/requests_closed.json"
        #url = "http://www.marcellison.com/json/requests.json"

        theJSON = urllib2.urlopen(url).read()
        reports = json.loads(theJSON)

        if not reports['service_requests']:
            print "*** NO DATA ***"
        print str(len(reports['service_requests'])) + " comments found"
        for reports in reports['service_requests']:
            ID = reports['service_request_id']
            serviceName = reports['service_name']
            status = reports['status']
            notes = reports['status_notes']
            requested_datetime = reports['requested_datetime']
            updated_datetime = reports['updated_datetime']
            expected_datetime = reports['expected_datetime']
            address = reports['address']
            longCoord = reports['long']
            latCoord = reports['lat']
            media = reports['media_url']
            
            #print ID, longCoord, latCoord, requested_datetime
            commentsUpdate(ID, serviceName, status, notes, requested_datetime, updated_datetime, expected_datetime, address, longCoord, latCoord, media)

        # Now check if request has been completed
        result = scraperwiki.sqlite.execute("SELECT serviceRequestID, status, requestDate, expectedDate, updatedDate FROM graffiti WHERE requestDate > ? ",(searchDate))
        commentsChecker(result)


def createTables():
    scraperwiki.sqlite.execute("create table graffiti (`serviceRequestID` string, `serviceName` string, `status` text, `statusNotes` text, `requestDate` text, `expectedDate` text, `updatedDate` text, `address` text, `addressLongitude` text, `addressLatitude` text, `mediaURL` text, `estimatedResponse` text, `delay` text)")
    scraperwiki.sqlite.execute("create table graffiti_temp (`serviceRequestID` string, `serviceName` string, `status` text, `statusNotes` text, `requestDate` text, `expectedDate` text, `updatedDate` text, `address` text, `addressLongitude` text, `addressLatitude` text, `mediaURL` text)")

def dropTables():
    scraperwiki.sqlite.execute("drop table if exists graffiti_temp")
    scraperwiki.sqlite.execute("drop table if exists graffiti")

def clear():
    dropTables()
    createTables()

#clear()
idGetter()
printOverdueResults()
printOverdueResults2()


