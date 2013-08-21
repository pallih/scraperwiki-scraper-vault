import scraperwiki
import time
from datetime import datetime, date, timedelta
import sys

# Setup database connections (max 10!)
scraperwiki.sqlite.attach("jobs_on_arbeitsagentur")
scraperwiki.sqlite.attach("jobs_on_dice")
scraperwiki.sqlite.attach("jobs_on_careerbuilder")
scraperwiki.sqlite.attach("jobs_on_careerbuilder_de")

# Calculate the sum of all jobs in all used lists
sumOfAllJobLists = 0
sumOfAllJobLists = sumOfAllJobLists + scraperwiki.sqlite.select('count(*) from jobs_on_careerbuilder.swdata')[0]["count(*)"]
sumOfAllJobLists = sumOfAllJobLists + scraperwiki.sqlite.select('count(*) from jobs_on_careerbuilder_de.swdata')[0]["count(*)"]
sumOfAllJobLists = sumOfAllJobLists + scraperwiki.sqlite.select('count(*) from jobs_on_arbeitsagentur.swdata')[0]["count(*)"]
sumOfAllJobLists = sumOfAllJobLists + scraperwiki.sqlite.select('count(*) from jobs_on_dice.swdata')[0]["count(*)"]
print "Total Number of Jobs: ", sumOfAllJobLists

# Global variables
count = 0
today = datetime.now()

# define methods
def saveRecords(records):
    global count
    for record in records:
        idNumber           = record["id"]
        dataAlreadySaved   = scraperwiki.sqlite.select("id from swdata where oldID='"+idNumber+"'", verbose=0)
        if dataAlreadySaved: continue
        record["oldID"]    = idNumber
        record["id"]       = None
        record["latitude"] = None
        record["longitude"]= None
        try: record["date"]
        except: record["date"] = today
        scraperwiki.sqlite.save(unique_keys=[], data=record, table_name='swdata', verbose=0)
        count = count + 1
        if count%1000 == 0: print count, " jobs processed. "
    return "Completed step: " + str(count)

# Setup database
#scraperwiki.sqlite.execute("drop table if exists swdata")
try:    scraperwiki.sqlite.execute("create table swdata (oldID, id INTEGER PRIMARY KEY AUTOINCREMENT)")
except: print "Table 'swdata' already exists."

# Start
print saveRecords(scraperwiki.sqlite.select('* from jobs_on_careerbuilder.swdata order by id desc'))
print saveRecords(scraperwiki.sqlite.select('* from jobs_on_careerbuilder_de.swdata order by id desc'))
print saveRecords(scraperwiki.sqlite.select('* from jobs_on_arbeitsagentur.swdata order by id desc'))
print saveRecords(scraperwiki.sqlite.select('* from jobs_on_dice.swdata order by id desc'))
print count, " jobs processed in total."

sys.exit()

# Cleanup
totalNumberOfJobs = scraperwiki.sqlite.select("count(*) from swdata")[0]["count(*)"]
scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (description IS NULL OR region IS NULL OR company IS NULL)")
scraperwiki.sqlite.execute("DELETE FROM swdata WHERE (description='' OR region='' OR company='')")
scraperwiki.sqlite.commit()
cleanedNumberOfJobs = scraperwiki.sqlite.select("count(*) from swdata")[0]["count(*)"]
print "Removed: ", totalNumberOfJobs - cleanedNumberOfJobs, " jobs without description, region or company."
