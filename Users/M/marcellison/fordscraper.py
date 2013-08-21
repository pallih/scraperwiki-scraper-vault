import scraperwiki
import re
import urllib
import urllib2
import simplejson as json
from datetime import date, timedelta

def commentsCounter():
        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBcomments WHERE killed = '1'")
        printResults()
        print result["data"][0][0], "comments were deleted from Mayor Ford's Facebook page."        
       
def commentsChecker(objectIDs):

        for each in objectIDs["data"]:
                objectID = each[0]
                results = scraperwiki.sqlite.execute("SELECT commentID FROM fordFBcomments WHERE objectID = ?",(objectID))
                for every in results["data"]:
                        commentID = every[0]
                        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBtemp WHERE objectID = ? AND commentID = ?",(objectID, commentID))
                     
                        if result["data"][0][0] == 0:
                                print "Comment was deleted."
                                scraperwiki.sqlite.execute("UPDATE fordFBcomments SET killed = '1' WHERE objectID = ? AND commentID = ?",(objectID, commentID))
                                scraperwiki.sqlite.commit()
                        else:
                                print "Comment NOT deleted."
                                pass

# Defines the function that processes the text using regular expressions and pulls out what we need, send it to the update
def commentsUpdate(objectID, commentID, commentName, commentNameID, commentMessage, commentCreated):

        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBcomments WHERE objectID = ? and commentID = ?", (objectID, commentID))
        test = result["data"]

        # this checks result in 'data' array
        if test[0][0] == 0:
                print "New comment. Adding to database."
                scraperwiki.sqlite.execute("insert into fordFBcomments values (?,?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID, "0"))
                scraperwiki.sqlite.execute("insert into fordFBtemp values (?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID))
                scraperwiki.sqlite.commit()

        else:
                print "Comment exists."
                scraperwiki.sqlite.execute("insert into fordFBtemp values (?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID))
                scraperwiki.sqlite.commit()

def commentGetter(objectID):
        limit = 50
        offset = 0

        while True:    
            url = "https://graph.facebook.com/" + objectID + "/comments?limit=" + str(limit) + "&offset=" + str(offset)
            print url
            c = urllib2.urlopen(url).read()
            fbcomments = json.loads(c)
            if not fbcomments['data']:
                print "*** NO DATA ***"
                break
            print str(len(fbcomments['data'])) + " comments found"
            for fbcomment in fbcomments['data']:
                commentID = fbcomment['id']
                commentName =  fbcomment['from']['name']
                commentNameID = fbcomment['from']['id']
                commentMessage = fbcomment['message']
                commentCreated = fbcomment['created_time']
                print commentID, commentName.encode('utf-8'), commentNameID, commentCreated
                commentsUpdate(objectID, commentID, commentName.encode('utf-8'), commentNameID, commentMessage.encode('utf-8'), commentCreated)

            offset = offset + 50  

def idGetter():

        scraperwiki.sqlite.execute("DELETE FROM fordFBtemp")
       
        todayDate = str(date.today())
        searchDate = str(date.today() - timedelta(days=12))

        url = "https://www.facebook.com/pages/Toronto-Mayor-Rob-Ford/142577519126992"

        response = urllib2.urlopen(url)
        the_page = response.read()
        print the_page

        # fbid":" Grabs objectIDs from main FB page, adds to the db if they are new
        for each in re.finditer("fbid&quot;:&quot;(.+?)&quot;", the_page):

                objectID = each.group(1)

                print objectID
                             
                result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBobj WHERE objectID = ?", (objectID))
                
                if result["data"][0][0] == 0:
                        print "New object. Adding to database."
                        scraperwiki.sqlite.execute("INSERT INTO fordFBobj (date_added, objectID) VALUES (?, ?)", (todayDate, objectID))
                        scraperwiki.sqlite.commit()
                else:
                        print "Object exists."

        # Pulls the list of n-day old items from the db, sends them to scraping
        result = scraperwiki.sqlite.execute("SELECT objectID FROM fordFBobj WHERE date_added > ? ",(searchDate))
        

        for each in result["data"]:
                objectID = each[0]
                print "**** SENDING THIS TO FB GRAPH "+objectID
                commentGetter(objectID)

        # Sends list of dates to check temp versus main tables in DB
        commentsChecker(result)


def createTables():
    scraperwiki.sqlite.execute("create table fordFBtemp (`commentID` string, `commentName` text, `commentNameID` text, `commentMessage` text, `commentCreated` text, `objectID` text)")
    scraperwiki.sqlite.execute("create table fordFBcomments (`commentID` string, `commentName` text, `commentNameID` text, `commentMessage` text, `commentCreated` text, `objectID` text, `killed` text)")
    scraperwiki.sqlite.execute("create table fordFBobj (`date_added` string, `objectID` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists fordFBtemp")
    scraperwiki.sqlite.execute("drop table if exists fordFBcomments")
    scraperwiki.sqlite.execute("drop table if exists fordFBobj")

def clear():
    dropTables()
    createTables()

def printResults():
    result = scraperwiki.sqlite.execute("SELECT commentCreated, commentMessage FROM fordFBcomments WHERE killed = '1' order by commentCreated asc")
    for each in result["data"]:
         print 'comment created: ' + each[0] + ', comment: ' + each[1]

idGetter()
commentsCounter()
import scraperwiki
import re
import urllib
import urllib2
import simplejson as json
from datetime import date, timedelta

def commentsCounter():
        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBcomments WHERE killed = '1'")
        printResults()
        print result["data"][0][0], "comments were deleted from Mayor Ford's Facebook page."        
       
def commentsChecker(objectIDs):

        for each in objectIDs["data"]:
                objectID = each[0]
                results = scraperwiki.sqlite.execute("SELECT commentID FROM fordFBcomments WHERE objectID = ?",(objectID))
                for every in results["data"]:
                        commentID = every[0]
                        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBtemp WHERE objectID = ? AND commentID = ?",(objectID, commentID))
                     
                        if result["data"][0][0] == 0:
                                print "Comment was deleted."
                                scraperwiki.sqlite.execute("UPDATE fordFBcomments SET killed = '1' WHERE objectID = ? AND commentID = ?",(objectID, commentID))
                                scraperwiki.sqlite.commit()
                        else:
                                print "Comment NOT deleted."
                                pass

# Defines the function that processes the text using regular expressions and pulls out what we need, send it to the update
def commentsUpdate(objectID, commentID, commentName, commentNameID, commentMessage, commentCreated):

        result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBcomments WHERE objectID = ? and commentID = ?", (objectID, commentID))
        test = result["data"]

        # this checks result in 'data' array
        if test[0][0] == 0:
                print "New comment. Adding to database."
                scraperwiki.sqlite.execute("insert into fordFBcomments values (?,?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID, "0"))
                scraperwiki.sqlite.execute("insert into fordFBtemp values (?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID))
                scraperwiki.sqlite.commit()

        else:
                print "Comment exists."
                scraperwiki.sqlite.execute("insert into fordFBtemp values (?,?,?,?,?,?)", (commentID, commentName, commentNameID, commentMessage, commentCreated, objectID))
                scraperwiki.sqlite.commit()

def commentGetter(objectID):
        limit = 50
        offset = 0

        while True:    
            url = "https://graph.facebook.com/" + objectID + "/comments?limit=" + str(limit) + "&offset=" + str(offset)
            print url
            c = urllib2.urlopen(url).read()
            fbcomments = json.loads(c)
            if not fbcomments['data']:
                print "*** NO DATA ***"
                break
            print str(len(fbcomments['data'])) + " comments found"
            for fbcomment in fbcomments['data']:
                commentID = fbcomment['id']
                commentName =  fbcomment['from']['name']
                commentNameID = fbcomment['from']['id']
                commentMessage = fbcomment['message']
                commentCreated = fbcomment['created_time']
                print commentID, commentName.encode('utf-8'), commentNameID, commentCreated
                commentsUpdate(objectID, commentID, commentName.encode('utf-8'), commentNameID, commentMessage.encode('utf-8'), commentCreated)

            offset = offset + 50  

def idGetter():

        scraperwiki.sqlite.execute("DELETE FROM fordFBtemp")
       
        todayDate = str(date.today())
        searchDate = str(date.today() - timedelta(days=12))

        url = "https://www.facebook.com/pages/Toronto-Mayor-Rob-Ford/142577519126992"

        response = urllib2.urlopen(url)
        the_page = response.read()
        print the_page

        # fbid":" Grabs objectIDs from main FB page, adds to the db if they are new
        for each in re.finditer("fbid&quot;:&quot;(.+?)&quot;", the_page):

                objectID = each.group(1)

                print objectID
                             
                result = scraperwiki.sqlite.execute("SELECT count(*) FROM fordFBobj WHERE objectID = ?", (objectID))
                
                if result["data"][0][0] == 0:
                        print "New object. Adding to database."
                        scraperwiki.sqlite.execute("INSERT INTO fordFBobj (date_added, objectID) VALUES (?, ?)", (todayDate, objectID))
                        scraperwiki.sqlite.commit()
                else:
                        print "Object exists."

        # Pulls the list of n-day old items from the db, sends them to scraping
        result = scraperwiki.sqlite.execute("SELECT objectID FROM fordFBobj WHERE date_added > ? ",(searchDate))
        

        for each in result["data"]:
                objectID = each[0]
                print "**** SENDING THIS TO FB GRAPH "+objectID
                commentGetter(objectID)

        # Sends list of dates to check temp versus main tables in DB
        commentsChecker(result)


def createTables():
    scraperwiki.sqlite.execute("create table fordFBtemp (`commentID` string, `commentName` text, `commentNameID` text, `commentMessage` text, `commentCreated` text, `objectID` text)")
    scraperwiki.sqlite.execute("create table fordFBcomments (`commentID` string, `commentName` text, `commentNameID` text, `commentMessage` text, `commentCreated` text, `objectID` text, `killed` text)")
    scraperwiki.sqlite.execute("create table fordFBobj (`date_added` string, `objectID` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists fordFBtemp")
    scraperwiki.sqlite.execute("drop table if exists fordFBcomments")
    scraperwiki.sqlite.execute("drop table if exists fordFBobj")

def clear():
    dropTables()
    createTables()

def printResults():
    result = scraperwiki.sqlite.execute("SELECT commentCreated, commentMessage FROM fordFBcomments WHERE killed = '1' order by commentCreated asc")
    for each in result["data"]:
         print 'comment created: ' + each[0] + ', comment: ' + each[1]

idGetter()
commentsCounter()
