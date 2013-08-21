import scraperwiki
import csv
import re
from collections import Counter

mainCounter = Counter()

def getTop10AnswersPerQuestion():

    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q1_support_statements.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q2_trail_use.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q3_trail_collision.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q4_20kph_limit.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q5_change_bylaw.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q6_use_lanes_for_what.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q7_change_bylaw2.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q8_sidewalks.csv")
    data = scraperwiki.scrape("http://www.marcellison.com/data/Q9_mobility_devices.csv")

    reader = csv.reader(data.splitlines())
    counter = 0
    

    for row in reader:
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            #print "looping - " + row[0]
            rowStripped = str(row).replace("['","")
            rowStripped = rowStripped.replace("']","")
            rowStripped = rowStripped.replace("'],","")
            stringList = re.split(',',rowStripped)
            mainCounter.update(stringList)
        counter += 1


    csvString = ""

    #print headers for CSV
    for letter, count in mainCounter.most_common(10):
        csvString = csvString + letter + "," + str(count) + "\n"
    print csvString

def insertCSV():
    scraperwiki.sqlite.execute("drop table if exists ebikeSurvey")
    scraperwiki.sqlite.execute("create table ebikeSurvey (`age` string, `sex` text, `health` text, `education` text, `income` text, `district` text, `distance` text, `time` text, `transport` text, `vehicle` text, `Q1` blob, `Q2` blob, `Q3` blob, `Q4` blob, `Q5` blob, `Q6` blob, `Q7` blob, `Q8` blob, `Q9` blob, `Q10` blob)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/ebike_survey_answers.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:

            #try:
                #14
            #unicode(row[14], "ascii")
            print "str(row[7]) = "+ str(row[7])
            print "str(row[8]) = "+ str(row[8])
            #except UnicodeDecodeError:
            #value = row[14].decode('latin1')
            #    print "UTF-8 = "+ value

            scraperwiki.sqlite.execute("INSERT INTO ebikeSurvey (age,sex,health,education,income,district,distance,time,transport,vehicle,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],str(row[10]).decode('latin1'),str(row[11]).decode('latin1'),str(row[12]).decode('latin1'),str(row[13]).decode('latin1'),str(row[14]).decode('latin1'),str(row[15]).decode('latin1'),str(row[16]).decode('latin1'),str(row[17]).decode('latin1'),str(row[18]).decode('latin1'),str(row[19]).decode('latin1')))
            scraperwiki.sqlite.commit()
        counter += 1


#run()
insertCSV()

import scraperwiki
import csv
import re
from collections import Counter

mainCounter = Counter()

def getTop10AnswersPerQuestion():

    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q1_support_statements.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q2_trail_use.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q3_trail_collision.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q4_20kph_limit.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q5_change_bylaw.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q6_use_lanes_for_what.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q7_change_bylaw2.csv")
    #data = scraperwiki.scrape("http://www.marcellison.com/data/Q8_sidewalks.csv")
    data = scraperwiki.scrape("http://www.marcellison.com/data/Q9_mobility_devices.csv")

    reader = csv.reader(data.splitlines())
    counter = 0
    

    for row in reader:
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            #print "looping - " + row[0]
            rowStripped = str(row).replace("['","")
            rowStripped = rowStripped.replace("']","")
            rowStripped = rowStripped.replace("'],","")
            stringList = re.split(',',rowStripped)
            mainCounter.update(stringList)
        counter += 1


    csvString = ""

    #print headers for CSV
    for letter, count in mainCounter.most_common(10):
        csvString = csvString + letter + "," + str(count) + "\n"
    print csvString

def insertCSV():
    scraperwiki.sqlite.execute("drop table if exists ebikeSurvey")
    scraperwiki.sqlite.execute("create table ebikeSurvey (`age` string, `sex` text, `health` text, `education` text, `income` text, `district` text, `distance` text, `time` text, `transport` text, `vehicle` text, `Q1` blob, `Q2` blob, `Q3` blob, `Q4` blob, `Q5` blob, `Q6` blob, `Q7` blob, `Q8` blob, `Q9` blob, `Q10` blob)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/ebike_survey_answers.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:

            #try:
                #14
            #unicode(row[14], "ascii")
            print "str(row[7]) = "+ str(row[7])
            print "str(row[8]) = "+ str(row[8])
            #except UnicodeDecodeError:
            #value = row[14].decode('latin1')
            #    print "UTF-8 = "+ value

            scraperwiki.sqlite.execute("INSERT INTO ebikeSurvey (age,sex,health,education,income,district,distance,time,transport,vehicle,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],str(row[10]).decode('latin1'),str(row[11]).decode('latin1'),str(row[12]).decode('latin1'),str(row[13]).decode('latin1'),str(row[14]).decode('latin1'),str(row[15]).decode('latin1'),str(row[16]).decode('latin1'),str(row[17]).decode('latin1'),str(row[18]).decode('latin1'),str(row[19]).decode('latin1')))
            scraperwiki.sqlite.commit()
        counter += 1


#run()
insertCSV()

