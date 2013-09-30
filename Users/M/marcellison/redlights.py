import scraperwiki
import csv


def run():
    scraperwiki.sqlite.execute("drop table if exists lights")
    scraperwiki.sqlite.execute("create table lights (`offenceDate` string, `dayOfWeek` text, `offenceTime` text, `plateID` text, `fine` text, `street` text, `city` text, `province` text, `latitude` text, `longitude` text)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/red_lights.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            scraperwiki.sqlite.execute("INSERT INTO lights (offenceDate,dayOfWeek,offenceTime,plateID,fine,street,city,province,latitude,longitude) VALUES (?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            scraperwiki.sqlite.commit()
        counter += 1


#run()

# numerous tickets!
#result = scraperwiki.sqlite.execute("select plateID, count(plateID) as plateCount from lights group by plateID having plateCount > 4")

# details of repeat offenders
#result = scraperwiki.sqlite.execute("select * from lights where plateID in (10512,20641,22328,23600,39438) order by plateID asc, offenceDate asc, offenceTime asc")

#result = scraperwiki.sqlite.execute("select count(*) from lights where fine = '' order by plateID asc, offenceDate asc, offenceTime asc")


#result = scraperwiki.sqlite.execute("select * from lights where street = 'BAYVIEW AVE. AND TRUMAN RD' and offenceDate = '08/07/12' order by offenceTime asc")

#result = scraperwiki.sqlite.execute("select latitude,longitude, count(*) as total from lights group by latitude,longitude")

result = scraperwiki.sqlite.execute("select offenceDate as total from lights street = 'JANE ST. AND BALA AVE'  group by latitude,longitude")

print str(result)

import scraperwiki
import csv


def run():
    scraperwiki.sqlite.execute("drop table if exists lights")
    scraperwiki.sqlite.execute("create table lights (`offenceDate` string, `dayOfWeek` text, `offenceTime` text, `plateID` text, `fine` text, `street` text, `city` text, `province` text, `latitude` text, `longitude` text)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/red_lights.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            scraperwiki.sqlite.execute("INSERT INTO lights (offenceDate,dayOfWeek,offenceTime,plateID,fine,street,city,province,latitude,longitude) VALUES (?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            scraperwiki.sqlite.commit()
        counter += 1


#run()

# numerous tickets!
#result = scraperwiki.sqlite.execute("select plateID, count(plateID) as plateCount from lights group by plateID having plateCount > 4")

# details of repeat offenders
#result = scraperwiki.sqlite.execute("select * from lights where plateID in (10512,20641,22328,23600,39438) order by plateID asc, offenceDate asc, offenceTime asc")

#result = scraperwiki.sqlite.execute("select count(*) from lights where fine = '' order by plateID asc, offenceDate asc, offenceTime asc")


#result = scraperwiki.sqlite.execute("select * from lights where street = 'BAYVIEW AVE. AND TRUMAN RD' and offenceDate = '08/07/12' order by offenceTime asc")

#result = scraperwiki.sqlite.execute("select latitude,longitude, count(*) as total from lights group by latitude,longitude")

result = scraperwiki.sqlite.execute("select offenceDate as total from lights street = 'JANE ST. AND BALA AVE'  group by latitude,longitude")

print str(result)

import scraperwiki
import csv


def run():
    scraperwiki.sqlite.execute("drop table if exists lights")
    scraperwiki.sqlite.execute("create table lights (`offenceDate` string, `dayOfWeek` text, `offenceTime` text, `plateID` text, `fine` text, `street` text, `city` text, `province` text, `latitude` text, `longitude` text)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/red_lights.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            scraperwiki.sqlite.execute("INSERT INTO lights (offenceDate,dayOfWeek,offenceTime,plateID,fine,street,city,province,latitude,longitude) VALUES (?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            scraperwiki.sqlite.commit()
        counter += 1


#run()

# numerous tickets!
#result = scraperwiki.sqlite.execute("select plateID, count(plateID) as plateCount from lights group by plateID having plateCount > 4")

# details of repeat offenders
#result = scraperwiki.sqlite.execute("select * from lights where plateID in (10512,20641,22328,23600,39438) order by plateID asc, offenceDate asc, offenceTime asc")

#result = scraperwiki.sqlite.execute("select count(*) from lights where fine = '' order by plateID asc, offenceDate asc, offenceTime asc")


#result = scraperwiki.sqlite.execute("select * from lights where street = 'BAYVIEW AVE. AND TRUMAN RD' and offenceDate = '08/07/12' order by offenceTime asc")

#result = scraperwiki.sqlite.execute("select latitude,longitude, count(*) as total from lights group by latitude,longitude")

result = scraperwiki.sqlite.execute("select offenceDate as total from lights street = 'JANE ST. AND BALA AVE'  group by latitude,longitude")

print str(result)

import scraperwiki
import csv


def run():
    scraperwiki.sqlite.execute("drop table if exists lights")
    scraperwiki.sqlite.execute("create table lights (`offenceDate` string, `dayOfWeek` text, `offenceTime` text, `plateID` text, `fine` text, `street` text, `city` text, `province` text, `latitude` text, `longitude` text)")

    data = scraperwiki.scrape("http://www.marcellison.com/data/red_lights.csv")
    reader = csv.reader(data.splitlines())

    #print reader[0]
    counter = 0

    for row in reader:
        #print (row[0])
        if counter == 0:
            print "DO NOTHING - HEADER ROW"
        else:
            scraperwiki.sqlite.execute("INSERT INTO lights (offenceDate,dayOfWeek,offenceTime,plateID,fine,street,city,province,latitude,longitude) VALUES (?,?,?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]))
            scraperwiki.sqlite.commit()
        counter += 1


#run()

# numerous tickets!
#result = scraperwiki.sqlite.execute("select plateID, count(plateID) as plateCount from lights group by plateID having plateCount > 4")

# details of repeat offenders
#result = scraperwiki.sqlite.execute("select * from lights where plateID in (10512,20641,22328,23600,39438) order by plateID asc, offenceDate asc, offenceTime asc")

#result = scraperwiki.sqlite.execute("select count(*) from lights where fine = '' order by plateID asc, offenceDate asc, offenceTime asc")


#result = scraperwiki.sqlite.execute("select * from lights where street = 'BAYVIEW AVE. AND TRUMAN RD' and offenceDate = '08/07/12' order by offenceTime asc")

#result = scraperwiki.sqlite.execute("select latitude,longitude, count(*) as total from lights group by latitude,longitude")

result = scraperwiki.sqlite.execute("select offenceDate as total from lights street = 'JANE ST. AND BALA AVE'  group by latitude,longitude")

print str(result)

