import calendar
import csv
import datetime
import scraperwiki

#scraperwiki.sqlite.execute("PRAGMA synchronous=OFF")
#scraperwiki.sqlite.execute("PRAGMA journal_mode=MEMORY")
#scraperwiki.sqlite.execute("BEGIN TRANSACTION")
scraperwiki.sqlite.execute("drop table 'Dates'")
scraperwiki.sqlite.execute("create table 'Dates'('title' text)")

holidays = ["September 2", "October 4", "October 14", "October 31", "November 1", "November 25",
            "November 26", "November 27",  "November 28",  "November 29", "December 13", "December 23",
            "December 24", "December 25", "December 26", "December 27", "December 30", "December 31",
            "January 1", "January 2", "January 3", "January 4", "January 5", "January 6",
            "January 20", "February 17", "February 18", "March 14", "March 28", "March 31",
            "April 1", "April 2", "April 3", "April 4", "April 18", "April 25"]

def holiday(date):
    if date.year not in xrange(2013, 2015):
        return True
    elif date.weekday() not in xrange(0, 5):
        return True
    elif date.year == 2013 and date.month in xrange(1, 8):
        return True
    elif date.year == 2014 and date.month in xrange(6, 13):
        return True
    elif date.month == 5 and date.day in xrange(24, 32):
        return True
    elif date.month == 8 and date.day in xrange(1, 8):
        return True
    elif date.strftime("%B %d") in holidays:
        return True
    else: 
        return False

def run(year):
    days = []
    for month in year:
        for weeks in month:
            for week in weeks:
                for day in week:
                    if not holiday(day):
                        entry = {}
                        entry["title"] = day.strftime("%A - %B %d, %Y")
                        entry["valid"] = True
                        if entry not in days:
                            days.append(entry)
    return days

def store_days(days):
    for day in days:
        entry = {}
        #print day["title"]
        entry["title"] = day["title"]
        scraperwiki.sqlite.save(unique_keys=['title'], data=entry, table_name="Dates")


cal = calendar.Calendar(2013)
year = cal.yeardatescalendar(2013)
days = run(year)
store_days(days)

cal = calendar.Calendar(2014)
year = cal.yeardatescalendar(2014)
days = run(year)
store_days(days)


with open('eggs.csv', 'wb') as csvfile:
    out = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    out.writerow(
    #out.writerow(['Spam'] * 5 + ['Baked Beans'])
    #out.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
import calendar
import csv
import datetime
import scraperwiki

#scraperwiki.sqlite.execute("PRAGMA synchronous=OFF")
#scraperwiki.sqlite.execute("PRAGMA journal_mode=MEMORY")
#scraperwiki.sqlite.execute("BEGIN TRANSACTION")
scraperwiki.sqlite.execute("drop table 'Dates'")
scraperwiki.sqlite.execute("create table 'Dates'('title' text)")

holidays = ["September 2", "October 4", "October 14", "October 31", "November 1", "November 25",
            "November 26", "November 27",  "November 28",  "November 29", "December 13", "December 23",
            "December 24", "December 25", "December 26", "December 27", "December 30", "December 31",
            "January 1", "January 2", "January 3", "January 4", "January 5", "January 6",
            "January 20", "February 17", "February 18", "March 14", "March 28", "March 31",
            "April 1", "April 2", "April 3", "April 4", "April 18", "April 25"]

def holiday(date):
    if date.year not in xrange(2013, 2015):
        return True
    elif date.weekday() not in xrange(0, 5):
        return True
    elif date.year == 2013 and date.month in xrange(1, 8):
        return True
    elif date.year == 2014 and date.month in xrange(6, 13):
        return True
    elif date.month == 5 and date.day in xrange(24, 32):
        return True
    elif date.month == 8 and date.day in xrange(1, 8):
        return True
    elif date.strftime("%B %d") in holidays:
        return True
    else: 
        return False

def run(year):
    days = []
    for month in year:
        for weeks in month:
            for week in weeks:
                for day in week:
                    if not holiday(day):
                        entry = {}
                        entry["title"] = day.strftime("%A - %B %d, %Y")
                        entry["valid"] = True
                        if entry not in days:
                            days.append(entry)
    return days

def store_days(days):
    for day in days:
        entry = {}
        #print day["title"]
        entry["title"] = day["title"]
        scraperwiki.sqlite.save(unique_keys=['title'], data=entry, table_name="Dates")


cal = calendar.Calendar(2013)
year = cal.yeardatescalendar(2013)
days = run(year)
store_days(days)

cal = calendar.Calendar(2014)
year = cal.yeardatescalendar(2014)
days = run(year)
store_days(days)


with open('eggs.csv', 'wb') as csvfile:
    out = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    out.writerow(
    #out.writerow(['Spam'] * 5 + ['Baked Beans'])
    #out.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
