'''
Created on Jul 10, 2012

@author: petrbouchal

Collect all data from No. 10 business plan API, build a database with this data, 
as well as with basic completion status data calculated, and deliver an analytical report on aggregates
and ideally with over-time analytics as well

'''

# TODO: finish readme

from calendar import monthrange

from bs4 import BeautifulSoup


# these switches let you control what is done:

writecsv = 0 # 0 to skip writing CSV; set to 0 for debugging download. Must be 0 for scraperwiki deployment
analytics = 0 # 1 to run aggregate analytics; set to 0 for debugging download/raw data write. Must be 0 for scraperwiki deployment
timeseriesanalytics = 0 # 1 to run time-series analytics. Must be 0 for scraperwiki deployment
checkchanges = 0 # set to 1 to check changes in duedates across downloads.
codebook = 0 # 1 to generate codebook
log = 1 # 1 to log
toscraperwiki = 1 # 1 for scraperwiki output

import scraperwiki

#import time
from datetime import datetime, timedelta
import csv
import json
import urllib2
import re
import shutil
import os
from pprint import pprint

#from pprint import pprint
now = datetime.now()
today = datetime.today()

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')
filedatestringlong = datetime.strftime(now, '%Y%m%d_%H%M%S')

# prepare CSV for writing
if writecsv == 1:
    csvout = "../output/BusinessPlans" + '_' + filedatestring + '.csv'
    csvout_final = '../output/BusinessPlans_current.csv'
    csvfile = open(csvout, 'wb')
    writer = csv.writer(csvfile, doublequote=True)
    # TODO: find way to push output to github directly, or alternatively Dropbox

# this list will be used to store all rows
alldata = []

# setup structure for assigning abbreviations to department names
deptdict = {}
deptdict['Department for Communities and Local Government'] = 'DCLG'
deptdict['Ministry of Justice'] = 'MoJ'
deptdict['Ministry of Defence'] = 'MoD'
deptdict['Cabinet Office'] = 'CO'
deptdict['Department of Energy and Climate Change'] = 'DECC'
deptdict['Department for Education'] = 'DfE'
deptdict['Department for Business, Innovation and Skills'] = 'BIS'
deptdict['Department for Transport'] = 'DfT'
deptdict['Her Majesty\'s Revenue and Customs'] = 'HMRC'
deptdict['Department for Work and Pensions'] = 'DWP'
deptdict['Department of Health'] = 'DH'
deptdict['Foreign and Commonwealth Office'] = 'FCO'
deptdict['Her Majesty\'s Treasury'] = 'HMT'
deptdict['Department for Environment, Food and Rural Affairs'] = 'Defra'
deptdict['Department for International Development'] = 'DfID'
deptdict['Department for Culture, Media and Sport'] = 'DCMS'
deptdict['Home Office'] = 'HO'

# build header
header = ['dept_abb', 'dept_name', 'dept_id', 'dept_url', 'priority_body', 'priority_id', \
          'priority_strapline', 'action_id', 'action_body', 'action_notes', \
          'schedule_start_date', 'schedule_end_date', 'actual_start_date', 'actual_end_date', 'subaction_id', 'subaction_body', \
          'subaction_notes', 'subaction_schedule_start_date', 'subaction_schedule_end_date', 'act_start', \
          'act_end', 'sched_start_endmonth', 'sched_end_endmonth', \
          'sched_duration', 'act_duration', 'duration_sofar', 'delta_duration', \
          'started', 'ended', 'start_status', 'end_status', 'startearlyby', 'startedlateby', 'startoverdueby', \
          'endearlyby', 'endedlateby', 'endoverdueby', \
          'duetostartthismonth', 'duetoendthismonth', 'duetostartwithin30days', 'duetoendwithin30days', \
          'duetostartlastmonth', 'duetoendinlast30days', 'duetoendlastmonth', 'duetoendinlast30days', \
          'startedthismonth', 'startedinlast30days', 'endedthismonth', 'endedinlast30days', \
          'carriedover', \
          'subaction_schedule_start_orig', 'subaction_schedule_end_orig', \
          'subaction_actual_start_orig', 'subaction_actual_end_orig', \
          'datetime', 'date']

if writecsv == 1:
    writer.writerow(header)

    rawdir = '../output/Raw_' + filedatestringlong
    os.makedirs(rawdir)

# Get list of departments
base_url = 'http://transparency.number10.gov.uk/api/'
urldepts = base_url + 'departments'
try:
    depts0 = urllib2.urlopen(urldepts)
except IOError:
    print('ERROR: API not available on initial call for department list.')
    writecsv = 0
    raise
depts = depts0.read()
deptsJ = json.loads(depts)


def savexml (filename, url):
    rawstore1 = open('./' + rawdir + '/' + filename + '.xml', 'wb')
    deptsxml = urllib2.urlopen(url + '.xml').read()
    rawstore1.write(deptsxml)
    rawstore1.close()
    return "OK"

if writecsv:
    savexml('departments', urldepts)

#get properties of each department
for dept in deptsJ:
    dept_id = dept['department_id']
    dept_name = dept['name']
    # TODO: Create dictionary for alternative department names 
    dept_url = dept['url']
    # get priorities for each department
    urlpriorities = base_url + 'priorities/department_id/' + str(dept_id)
    try:
        priorities0 = urllib2.urlopen(urlpriorities)
    except IOError:
        print('ERROR: API not available on call for priorities.')
        writecsv = 0
        raise
    priorities = priorities0.read()
    prioritiesJ = json.loads(priorities)

    if writecsv:
        savexml('priorities_' + deptdict[dept_name], urlpriorities)

    #pprint.pprint(prioritiesJ)
    # get properties of each priority
    for priority in prioritiesJ:
        priority_body = priority['body']
        priority_id = priority['priority_id']
        priority_strapline = priority['strapline']
        # get actions for each priority
        urlactions = base_url + 'actions/priority_id/' + str(priority_id)
        try:
            actions0 = urllib2.urlopen(urlactions)
        except IOError:
            print('ERROR: API not available when retrieving actions.')
            writecsv = 0
            raise
        actions = actions0.read()
        actionsJ = json.loads(actions)

        if writecsv:
            savexml('actions_dept_' + deptdict[dept_name] + '_priority_' + str(priority_id), urlactions)

        # get properties of each action
        for action in actionsJ:
            action_id = action['action_id']
            actual_end_date = action['actual_end_date']
            actual_start_date = action['actual_start_date']
            action_body = action['body']
            action_notes = action['notes']
            schedule_end_date = action['schedule_end_date']
            schedule_start_date = action['schedule_start_date']
            # cycle through sub-actions
            for subaction in action['sub_actions']:
                subaction_id = subaction['action_id']
                subaction_actual_end_date = subaction['actual_end_date']
                subaction_actual_start_date = subaction['actual_start_date']
                subaction_body = subaction['body']
                subaction_notes = subaction['notes']
                subaction_schedule_end_date = subaction['schedule_end_date']
                subaction_schedule_start_date = subaction['schedule_start_date']

                subaction_actual_end_date_orig = subaction_actual_end_date
                subaction_actual_start_date_orig = subaction_actual_end_date
                subaction_schedule_end_date_orig = subaction_actual_end_date
                subaction_schedule_start_date_orig = subaction_actual_end_date

                #===========================================================
                # FIX DATES
                #===========================================================

                # convert seasons to months
                # TODO: devise more robust date processing, probably by using dateutil.parser

                subaction_schedule_start_date = subaction_schedule_start_date.replace('Winter 2012', 'Dec 2012')\
                .replace('Spring', 'Apr').replace('Summer', 'Jul').replace('Autumn', 'Oct')

                subaction_schedule_end_date = subaction_schedule_end_date.replace('Winter 2012', 'Dec 2012')\
                .replace('Spring', 'Apr').replace('Summer', 'Jul').replace('Autumn', 'Oct')

                #fix known typos in scheduled date fields
                subaction_schedule_end_date = subaction_schedule_end_date.replace('Sep 212', 'Sep 2012').replace('Octo', 'Oct')

                # process scheduled dates
                sched_start_text = False
                sched_end_text = False
                try:
                    # trying if the date is in Apr 13 type format ...
                    #
                    # NOTE dates whose name end in 0 are date objects, other date variables are strings
                    #
                    sched_end0 = datetime.strptime(subaction_schedule_end_date, '%b %Y')
                    sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
                except ValueError:
                    # ... or in April 14 format:
                    try:
                        sched_end0 = datetime.strptime(subaction_schedule_end_date, '%B %Y')
                        sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
                    except ValueError:
                        sched_end = 'NA'
                        sched_end_text = True

                try:
                # same for start date - turn into real data and format correctly
                    sched_start0 = datetime.strptime(subaction_schedule_start_date, '%b %Y')
                    sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
                except ValueError:
                    try:
                        sched_start0 = datetime.strptime(subaction_schedule_start_date, '%B %Y')
                        sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
                    except ValueError:
                        sched_start = 'NA'
                        sched_start_text = True

                if sched_start_text != True:
                    sched_start_day = sched_start0.day
                    sched_start_month = sched_start0.month
                    sched_start_year = sched_start0.year
                    sched_start_numberofdays = int(monthrange(sched_start_year, int(sched_start_month))[1])
                    sched_start_endmonth0 = sched_start0.replace(day=sched_start_numberofdays)
                    sched_start_endmonth = datetime.strftime(sched_start_endmonth0, '%Y-%m-%d')
                else:
                    sched_start_endmonth0 = 'NA'
                    sched_start_endmonth = 'NA'

                if sched_end_text != True:
                    sched_end_day = sched_end0.day
                    sched_end_month = sched_end0.month
                    sched_end_year = sched_end0.year
                    sched_end_numberofdays = int(monthrange(sched_end_year, int(sched_end_month))[1])
                    sched_end_endmonth0 = sched_end0.replace(day=sched_end_numberofdays)
                    sched_end_endmonth = datetime.strftime(sched_end_endmonth0, '%Y-%m-%d')
                else:
                    sched_end_endmonth0 = 'NA'
                    sched_end_endmonth = 'NA'

                # process actual dates - turn into real dates and get rid of time component
                try:
                    act_start0 = datetime.strptime(subaction_actual_start_date, '%Y-%m-%d %H:%M:%S')
                    act_start = datetime.strftime(act_start0, '%Y-%m-%d')
                except TypeError:
                    act_start = 'NA'
                    act_start0 = 'NA'
                except ValueError:
                    act_start = 'NA'
                    act_start0 = 'NA'

                try:
                    act_end0 = datetime.strptime(subaction_actual_end_date, '%Y-%m-%d %H:%M:%S')
                    act_end = datetime.strftime(act_end0, '%Y-%m-%d')
                except ValueError:
                    act_end = 'NA'
                    act_end0 = 'NA'
                except TypeError:
                    act_end = 'NA'
                    act_end0 = 'NA'

                #===============================================================================
                # BASIC ANALYTICS: MARK EACH ITEM WITH STATUS CODES
                #===============================================================================

                print 'Subaction ID: ' + str(subaction_id)
                print urlactions

                start_status = 'NA'
                end_status = 'NA'
                carriedover = 0

                # calculate scheduled duration
                # TODO: change duration counting and comparisons to MONTHS
                if ((sched_end_text == False) & (sched_start_text == False)):
                    sched_duration = (sched_end_endmonth0 - sched_start0).days
                else:
                    sched_duration = 'NA'

                # first the start

                if act_start != 'NA':
                    started = True
                else:
                    started = False

                if subaction_schedule_start_date == "Started":
                    sched_start_text = True
                    started = True
                    start_status = 'Carried over'
                    carriedover = 1
                elif subaction_schedule_start_date == 'TBC':
                    start_status = 'TBC'
                    sched_start_text = True


                if ((started == True) & (sched_start_text == False)):
                    startedoverdueby = 'NA'
                    startduein = 'NA'
                    if ((sched_start_endmonth0.month > act_start0.month) & (sched_start_endmonth0 > act_start0)):
                        start_status = 'Early'
                        startearlyby = (sched_start0 - act_start0).days
                    elif ((sched_start_endmonth0 >= act_start0) & (sched_start_endmonth0.month == act_start0.month)):
                        start_status = 'On time'
                        startearlyby = 'NA'
                        startedlateby = 'NA'
                    elif sched_start_endmonth0 < act_start0:
                        start_status = 'Late'
                        startedlateby = (act_start0 - sched_start_endmonth0).days
                        startearlyby = 'NA'
                elif ((started == False) & (sched_start_text == False)):
                    startedlateby = 'NA'
                    startearlyby = 'NA'
                    if sched_start_endmonth0 > today:
                        start_status = 'Not due'
                        startoverdueby = 'NA'
                        startduein = (sched_start_endmonth0 - today).days
                    elif sched_start_endmonth0 < today:
                        start_status = 'Overdue'
                        startduein = ''
                        startoverdueby = (today - sched_start_endmonth0).days
                elif ((started == True) & (sched_start_text == True)):
                    startearlyby = 'NA'
                    startoverdueby = 'NA'
                    startedlateby = 'NA'
                    startduein = 'NA'
                elif ((started == False) & (sched_start_text == True)):
                    startearlyby = 'NA'
                    startoverdueby = 'NA'
                    startedlateby = 'NA'
                    startduein = 'NA'

                # now the end
                if subaction_schedule_end_date == 'Ongoing':
                    end_status = 'Ongoing'
                    sched_end_text = True
                    ended = False
                elif subaction_schedule_end_date == 'TBC':
                    end_status = 'TBC'
                    sched_end_text = True
                    ended = False
                elif act_end == 'NA':
                    ended = False

                if act_end != 'NA':
                    ended = True
                else:
                    ended = False

                if (ended == True) & (sched_end_text != True):
                    endedoverdueby = 'NA'
                    endduein = 'NA'
                    if ((sched_end_endmonth0.month > act_end0.month) & (sched_end_endmonth0 > act_end0)):
                        end_status = 'Early'
                        endedlateby = 'NA'
                        endearlyby = (sched_end0 - act_end0).days
                    elif ((sched_end_endmonth0 >= act_end0) & (sched_end_endmonth0.month == act_end0.month)):
                        end_status = 'On time'
                        endedlateby = 'NA'
                        endearlyby = 'NA'
                    elif sched_end_endmonth < act_end:
                        end_status = 'Late'
                        endearlyby = 'NA'
                        endedlateby = (act_end0 - sched_end_endmonth0).days
                elif ((ended == False) & (sched_end_text != True)):
                    endedlateby = 'NA'
                    endearlyby = 'NA'
                    if sched_end_endmonth0 >= today:
                        end_status = 'Not due'
                        endedoverdueby = 'NA'
                        endduein = (sched_end_endmonth0 - today).days
                    elif sched_end_endmonth0 < today:
                        end_status = 'Overdue'
                        endduein = 'NA'
                        endedoverdueby = (today - sched_end_endmonth0).days
                elif ((ended == True) & (sched_end_text == True)):
                    endearlyby = 'NA'
                    endedoverdueby = 'NA'
                    endedlateby = 'NA'
                    endduein = 'NA'
                elif ((ended == False) & (sched_end_text == True)):
                    endearlyby = 'NA'
                    endedoverdueby = 'NA'
                    endedlateby = 'NA'
                    endduein = 'NA'

                # calculate actual duration and compare to scheduled
                if ((started == True) & (ended == True) & (sched_start_text == False)):
                    act_duration = (act_end0 - act_start0).days + 1
                    duration_sofar = 'NA'
                elif ((started == True) & (ended == False) & (sched_start_text == False)):
                    act_duration = 'NA'
                    duration_sofar = (today - act_start0).days + 1
                else:
                    act_duration = 'NA'
                    duration_sofar = 'NA'

                if ((sched_duration != 'NA') & (duration_sofar != 'NA')):
                    delta_duration = (duration_sofar - sched_duration)
                    # positive number means action overran the scheduled length
                elif ((sched_duration != 'NA') & (act_duration != 'NA')):
                    delta_duration = (act_duration - sched_duration)
                    # positive number means action overran the scheduled length
                else:
                    delta_duration = 'NA'

                # Mark those due to start this month and in next 30 days
                if ((started == False) & (sched_start_text != 1)):
                    duetostartthismonth = ((sched_start_endmonth0.month == today.month) & (sched_start_endmonth0.year == today.year))
                    duetostartwithin30days = (sched_start_endmonth0 < today - timedelta(days=30))
                else:
                    duetostartthismonth = 'NA'
                    duetostartwithin30days = 'NA'

                if ((sched_start_text != 1)):
                    duetostartlastmonth = ((sched_start_endmonth0.month == today.month - 1) & (sched_start_endmonth0.year == today.year))
                    duetostartinlast30days = (sched_start_endmonth0 < today - timedelta(days=30))
                else:
                    duetostartlastmonth = 'NA'
                    duetostartinlast30days = 'NA'

                # TODO: due to end/ended/due to start/started LAST MONTH
                if ((ended == False) & (sched_end_text != 1)):
                    duetoendthismonth = ((sched_end_endmonth0.month == today.month) & (sched_end_endmonth0.year == today.year))
                    duetoendwithin30days = (sched_end_endmonth0 < today - timedelta(days=30))
                else:
                    duetoendthismonth = 'NA'
                    duetoendwithin30days = 'NA'

                if ((sched_end_text != 1)):
                    duetoendlastmonth = ((sched_end_endmonth0.month == today.month - 1) & (sched_end_endmonth0.year == today.year))
                    duetoendinlast30days = (sched_end_endmonth0 < today - timedelta(days=30))
                else:
                    duetoendlastmonth = 'NA'
                    duetoendinlast30days = 'NA'

                # Mark those started or ended this month and in last 30 days
                if ((started == True) & (sched_start_text == False)):
                    startedthismonth = ((act_start0.month == today.month) & (sched_start_endmonth0.year == today.year))
                    startedinlast30days = (act_start0 < today - timedelta(days=30))
                else:
                    startedthismonth = 'NA'
                    startedinlast30days = 'NA'

                if ((ended == True) & (sched_end_text == False)):
                    endedthismonth = ((act_end0.month == today.month) & (sched_end_endmonth0.year == today.year))
                    endedinlast30days = (act_end0 < today - timedelta(days=30))
                else:
                    endedthismonth = 'NA'
                    endedinlast30days = 'NA'

                # TODO: but still write the end-of-month dates because of excel

                #===================================================================
                # WRITE PROCESSED RESULT TO CSV
                #===================================================================

                dept_abb = deptdict[dept_name]

                # build row
                row0 = [dept_abb, dept_name, dept_id, dept_url, priority_body, priority_id, priority_strapline, action_id, action_body, \
                       action_notes, schedule_start_date, schedule_end_date, actual_start_date, actual_end_date, subaction_id, \
                       subaction_body, subaction_notes, subaction_schedule_start_date, subaction_schedule_end_date, \
                       act_start, act_end, sched_start_endmonth, sched_end_endmonth, \
                       sched_duration, act_duration, duration_sofar, delta_duration, \
                       started, ended, start_status, end_status, startearlyby, startedlateby, startoverdueby, \
                       endearlyby, endedlateby, endedoverdueby, \
                       duetostartthismonth, duetoendthismonth, duetostartwithin30days, duetoendwithin30days, \
                       duetostartlastmonth, duetoendinlast30days, duetoendlastmonth, duetoendinlast30days, \
                       startedthismonth, startedinlast30days, endedthismonth, endedinlast30days, \
                       carriedover, # add new stuff here - it won't throw off the counting of items in the analytics\
                       subaction_schedule_start_date_orig, subaction_schedule_end_date_orig, \
                       subaction_actual_start_date_orig, subaction_actual_end_date_orig, \
                       datetimestring, datestring]

                # clean output of HMTL tags and entities
                # FIXME: make this cleanup work so it replaces all entities - the unescape solution is not robust

                row = []
                for cell in row0:
                    if isinstance(cell, basestring):
                        t = cell
                        # get rid of HTML coded entities which break R imports
                        cellsoup = BeautifulSoup(cell)
                        text_parts = cellsoup.findAll(text=True)
                        textcell = ' '.join(text_parts)
                        t1 = textcell
                        #t = re.sub(textcell, '\n', '')
                        t0 = t1.replace(' & #39;', '\'').replace('&amp;#39;', '\'').replace('&amp;#40;', '\'').replace('&amp;#41;', '\'')
                        t = t0.replace('\r\n', ' ').replace('\n', ' ')
                        # FIXME: remove newline characters from within the resulting text
                        # TODO: check whether text within tags is not being lost
                    elif isinstance(cell, bool):
                        # replace boolean values with 0/1 for easy averaging in excel
                        if cell == True:
                            t = 1
                        else:
                            t = 0

                    else:
                        t = cell
                    row.append(t)

                # write row
                if writecsv == 1:
                    writer.writerow(row)
                else:
                    print('NOTE: no CSV writing done - test run only. See switch at start of script')

                rowDict = dict(zip(header, row0))

                if toscraperwiki == 1:
                    scraperwiki.sqlite.save(unique_keys=['subaction_id', 'datetime'],data=rowDict, table_name='Actions')

                # add row to list of rows if needed for analytics
                if ((analytics == 1) | (timeseriesanalytics == 1)):
                    alldata.append(row0)
if writecsv == 1:
    csvfile.close()
    shutil.copy(csvout, csvout_final)

#===============================================================================
# #===============================================================================
# # ADVANCED ANALYTICS 1: GETTING THE TOP-LEVEL AGGREGATE FIGURES
# #===============================================================================
#===============================================================================

if analytics == 1:
    print "Starting analytics..."
    execfile("./bp_analytics.py")

if timeseriesanalytics != 0:
    print 'Starting analytics'
    execfile("bp_timeseries.py")

# TODO: build log of what was downloaded/calculated from where and when    
'''
Created on Jul 10, 2012

@author: petrbouchal

Collect all data from No. 10 business plan API, build a database with this data, 
as well as with basic completion status data calculated, and deliver an analytical report on aggregates
and ideally with over-time analytics as well

'''

# TODO: finish readme

from calendar import monthrange

from bs4 import BeautifulSoup


# these switches let you control what is done:

writecsv = 0 # 0 to skip writing CSV; set to 0 for debugging download. Must be 0 for scraperwiki deployment
analytics = 0 # 1 to run aggregate analytics; set to 0 for debugging download/raw data write. Must be 0 for scraperwiki deployment
timeseriesanalytics = 0 # 1 to run time-series analytics. Must be 0 for scraperwiki deployment
checkchanges = 0 # set to 1 to check changes in duedates across downloads.
codebook = 0 # 1 to generate codebook
log = 1 # 1 to log
toscraperwiki = 1 # 1 for scraperwiki output

import scraperwiki

#import time
from datetime import datetime, timedelta
import csv
import json
import urllib2
import re
import shutil
import os
from pprint import pprint

#from pprint import pprint
now = datetime.now()
today = datetime.today()

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')
filedatestringlong = datetime.strftime(now, '%Y%m%d_%H%M%S')

# prepare CSV for writing
if writecsv == 1:
    csvout = "../output/BusinessPlans" + '_' + filedatestring + '.csv'
    csvout_final = '../output/BusinessPlans_current.csv'
    csvfile = open(csvout, 'wb')
    writer = csv.writer(csvfile, doublequote=True)
    # TODO: find way to push output to github directly, or alternatively Dropbox

# this list will be used to store all rows
alldata = []

# setup structure for assigning abbreviations to department names
deptdict = {}
deptdict['Department for Communities and Local Government'] = 'DCLG'
deptdict['Ministry of Justice'] = 'MoJ'
deptdict['Ministry of Defence'] = 'MoD'
deptdict['Cabinet Office'] = 'CO'
deptdict['Department of Energy and Climate Change'] = 'DECC'
deptdict['Department for Education'] = 'DfE'
deptdict['Department for Business, Innovation and Skills'] = 'BIS'
deptdict['Department for Transport'] = 'DfT'
deptdict['Her Majesty\'s Revenue and Customs'] = 'HMRC'
deptdict['Department for Work and Pensions'] = 'DWP'
deptdict['Department of Health'] = 'DH'
deptdict['Foreign and Commonwealth Office'] = 'FCO'
deptdict['Her Majesty\'s Treasury'] = 'HMT'
deptdict['Department for Environment, Food and Rural Affairs'] = 'Defra'
deptdict['Department for International Development'] = 'DfID'
deptdict['Department for Culture, Media and Sport'] = 'DCMS'
deptdict['Home Office'] = 'HO'

# build header
header = ['dept_abb', 'dept_name', 'dept_id', 'dept_url', 'priority_body', 'priority_id', \
          'priority_strapline', 'action_id', 'action_body', 'action_notes', \
          'schedule_start_date', 'schedule_end_date', 'actual_start_date', 'actual_end_date', 'subaction_id', 'subaction_body', \
          'subaction_notes', 'subaction_schedule_start_date', 'subaction_schedule_end_date', 'act_start', \
          'act_end', 'sched_start_endmonth', 'sched_end_endmonth', \
          'sched_duration', 'act_duration', 'duration_sofar', 'delta_duration', \
          'started', 'ended', 'start_status', 'end_status', 'startearlyby', 'startedlateby', 'startoverdueby', \
          'endearlyby', 'endedlateby', 'endoverdueby', \
          'duetostartthismonth', 'duetoendthismonth', 'duetostartwithin30days', 'duetoendwithin30days', \
          'duetostartlastmonth', 'duetoendinlast30days', 'duetoendlastmonth', 'duetoendinlast30days', \
          'startedthismonth', 'startedinlast30days', 'endedthismonth', 'endedinlast30days', \
          'carriedover', \
          'subaction_schedule_start_orig', 'subaction_schedule_end_orig', \
          'subaction_actual_start_orig', 'subaction_actual_end_orig', \
          'datetime', 'date']

if writecsv == 1:
    writer.writerow(header)

    rawdir = '../output/Raw_' + filedatestringlong
    os.makedirs(rawdir)

# Get list of departments
base_url = 'http://transparency.number10.gov.uk/api/'
urldepts = base_url + 'departments'
try:
    depts0 = urllib2.urlopen(urldepts)
except IOError:
    print('ERROR: API not available on initial call for department list.')
    writecsv = 0
    raise
depts = depts0.read()
deptsJ = json.loads(depts)


def savexml (filename, url):
    rawstore1 = open('./' + rawdir + '/' + filename + '.xml', 'wb')
    deptsxml = urllib2.urlopen(url + '.xml').read()
    rawstore1.write(deptsxml)
    rawstore1.close()
    return "OK"

if writecsv:
    savexml('departments', urldepts)

#get properties of each department
for dept in deptsJ:
    dept_id = dept['department_id']
    dept_name = dept['name']
    # TODO: Create dictionary for alternative department names 
    dept_url = dept['url']
    # get priorities for each department
    urlpriorities = base_url + 'priorities/department_id/' + str(dept_id)
    try:
        priorities0 = urllib2.urlopen(urlpriorities)
    except IOError:
        print('ERROR: API not available on call for priorities.')
        writecsv = 0
        raise
    priorities = priorities0.read()
    prioritiesJ = json.loads(priorities)

    if writecsv:
        savexml('priorities_' + deptdict[dept_name], urlpriorities)

    #pprint.pprint(prioritiesJ)
    # get properties of each priority
    for priority in prioritiesJ:
        priority_body = priority['body']
        priority_id = priority['priority_id']
        priority_strapline = priority['strapline']
        # get actions for each priority
        urlactions = base_url + 'actions/priority_id/' + str(priority_id)
        try:
            actions0 = urllib2.urlopen(urlactions)
        except IOError:
            print('ERROR: API not available when retrieving actions.')
            writecsv = 0
            raise
        actions = actions0.read()
        actionsJ = json.loads(actions)

        if writecsv:
            savexml('actions_dept_' + deptdict[dept_name] + '_priority_' + str(priority_id), urlactions)

        # get properties of each action
        for action in actionsJ:
            action_id = action['action_id']
            actual_end_date = action['actual_end_date']
            actual_start_date = action['actual_start_date']
            action_body = action['body']
            action_notes = action['notes']
            schedule_end_date = action['schedule_end_date']
            schedule_start_date = action['schedule_start_date']
            # cycle through sub-actions
            for subaction in action['sub_actions']:
                subaction_id = subaction['action_id']
                subaction_actual_end_date = subaction['actual_end_date']
                subaction_actual_start_date = subaction['actual_start_date']
                subaction_body = subaction['body']
                subaction_notes = subaction['notes']
                subaction_schedule_end_date = subaction['schedule_end_date']
                subaction_schedule_start_date = subaction['schedule_start_date']

                subaction_actual_end_date_orig = subaction_actual_end_date
                subaction_actual_start_date_orig = subaction_actual_end_date
                subaction_schedule_end_date_orig = subaction_actual_end_date
                subaction_schedule_start_date_orig = subaction_actual_end_date

                #===========================================================
                # FIX DATES
                #===========================================================

                # convert seasons to months
                # TODO: devise more robust date processing, probably by using dateutil.parser

                subaction_schedule_start_date = subaction_schedule_start_date.replace('Winter 2012', 'Dec 2012')\
                .replace('Spring', 'Apr').replace('Summer', 'Jul').replace('Autumn', 'Oct')

                subaction_schedule_end_date = subaction_schedule_end_date.replace('Winter 2012', 'Dec 2012')\
                .replace('Spring', 'Apr').replace('Summer', 'Jul').replace('Autumn', 'Oct')

                #fix known typos in scheduled date fields
                subaction_schedule_end_date = subaction_schedule_end_date.replace('Sep 212', 'Sep 2012').replace('Octo', 'Oct')

                # process scheduled dates
                sched_start_text = False
                sched_end_text = False
                try:
                    # trying if the date is in Apr 13 type format ...
                    #
                    # NOTE dates whose name end in 0 are date objects, other date variables are strings
                    #
                    sched_end0 = datetime.strptime(subaction_schedule_end_date, '%b %Y')
                    sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
                except ValueError:
                    # ... or in April 14 format:
                    try:
                        sched_end0 = datetime.strptime(subaction_schedule_end_date, '%B %Y')
                        sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
                    except ValueError:
                        sched_end = 'NA'
                        sched_end_text = True

                try:
                # same for start date - turn into real data and format correctly
                    sched_start0 = datetime.strptime(subaction_schedule_start_date, '%b %Y')
                    sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
                except ValueError:
                    try:
                        sched_start0 = datetime.strptime(subaction_schedule_start_date, '%B %Y')
                        sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
                    except ValueError:
                        sched_start = 'NA'
                        sched_start_text = True

                if sched_start_text != True:
                    sched_start_day = sched_start0.day
                    sched_start_month = sched_start0.month
                    sched_start_year = sched_start0.year
                    sched_start_numberofdays = int(monthrange(sched_start_year, int(sched_start_month))[1])
                    sched_start_endmonth0 = sched_start0.replace(day=sched_start_numberofdays)
                    sched_start_endmonth = datetime.strftime(sched_start_endmonth0, '%Y-%m-%d')
                else:
                    sched_start_endmonth0 = 'NA'
                    sched_start_endmonth = 'NA'

                if sched_end_text != True:
                    sched_end_day = sched_end0.day
                    sched_end_month = sched_end0.month
                    sched_end_year = sched_end0.year
                    sched_end_numberofdays = int(monthrange(sched_end_year, int(sched_end_month))[1])
                    sched_end_endmonth0 = sched_end0.replace(day=sched_end_numberofdays)
                    sched_end_endmonth = datetime.strftime(sched_end_endmonth0, '%Y-%m-%d')
                else:
                    sched_end_endmonth0 = 'NA'
                    sched_end_endmonth = 'NA'

                # process actual dates - turn into real dates and get rid of time component
                try:
                    act_start0 = datetime.strptime(subaction_actual_start_date, '%Y-%m-%d %H:%M:%S')
                    act_start = datetime.strftime(act_start0, '%Y-%m-%d')
                except TypeError:
                    act_start = 'NA'
                    act_start0 = 'NA'
                except ValueError:
                    act_start = 'NA'
                    act_start0 = 'NA'

                try:
                    act_end0 = datetime.strptime(subaction_actual_end_date, '%Y-%m-%d %H:%M:%S')
                    act_end = datetime.strftime(act_end0, '%Y-%m-%d')
                except ValueError:
                    act_end = 'NA'
                    act_end0 = 'NA'
                except TypeError:
                    act_end = 'NA'
                    act_end0 = 'NA'

                #===============================================================================
                # BASIC ANALYTICS: MARK EACH ITEM WITH STATUS CODES
                #===============================================================================

                print 'Subaction ID: ' + str(subaction_id)
                print urlactions

                start_status = 'NA'
                end_status = 'NA'
                carriedover = 0

                # calculate scheduled duration
                # TODO: change duration counting and comparisons to MONTHS
                if ((sched_end_text == False) & (sched_start_text == False)):
                    sched_duration = (sched_end_endmonth0 - sched_start0).days
                else:
                    sched_duration = 'NA'

                # first the start

                if act_start != 'NA':
                    started = True
                else:
                    started = False

                if subaction_schedule_start_date == "Started":
                    sched_start_text = True
                    started = True
                    start_status = 'Carried over'
                    carriedover = 1
                elif subaction_schedule_start_date == 'TBC':
                    start_status = 'TBC'
                    sched_start_text = True


                if ((started == True) & (sched_start_text == False)):
                    startedoverdueby = 'NA'
                    startduein = 'NA'
                    if ((sched_start_endmonth0.month > act_start0.month) & (sched_start_endmonth0 > act_start0)):
                        start_status = 'Early'
                        startearlyby = (sched_start0 - act_start0).days
                    elif ((sched_start_endmonth0 >= act_start0) & (sched_start_endmonth0.month == act_start0.month)):
                        start_status = 'On time'
                        startearlyby = 'NA'
                        startedlateby = 'NA'
                    elif sched_start_endmonth0 < act_start0:
                        start_status = 'Late'
                        startedlateby = (act_start0 - sched_start_endmonth0).days
                        startearlyby = 'NA'
                elif ((started == False) & (sched_start_text == False)):
                    startedlateby = 'NA'
                    startearlyby = 'NA'
                    if sched_start_endmonth0 > today:
                        start_status = 'Not due'
                        startoverdueby = 'NA'
                        startduein = (sched_start_endmonth0 - today).days
                    elif sched_start_endmonth0 < today:
                        start_status = 'Overdue'
                        startduein = ''
                        startoverdueby = (today - sched_start_endmonth0).days
                elif ((started == True) & (sched_start_text == True)):
                    startearlyby = 'NA'
                    startoverdueby = 'NA'
                    startedlateby = 'NA'
                    startduein = 'NA'
                elif ((started == False) & (sched_start_text == True)):
                    startearlyby = 'NA'
                    startoverdueby = 'NA'
                    startedlateby = 'NA'
                    startduein = 'NA'

                # now the end
                if subaction_schedule_end_date == 'Ongoing':
                    end_status = 'Ongoing'
                    sched_end_text = True
                    ended = False
                elif subaction_schedule_end_date == 'TBC':
                    end_status = 'TBC'
                    sched_end_text = True
                    ended = False
                elif act_end == 'NA':
                    ended = False

                if act_end != 'NA':
                    ended = True
                else:
                    ended = False

                if (ended == True) & (sched_end_text != True):
                    endedoverdueby = 'NA'
                    endduein = 'NA'
                    if ((sched_end_endmonth0.month > act_end0.month) & (sched_end_endmonth0 > act_end0)):
                        end_status = 'Early'
                        endedlateby = 'NA'
                        endearlyby = (sched_end0 - act_end0).days
                    elif ((sched_end_endmonth0 >= act_end0) & (sched_end_endmonth0.month == act_end0.month)):
                        end_status = 'On time'
                        endedlateby = 'NA'
                        endearlyby = 'NA'
                    elif sched_end_endmonth < act_end:
                        end_status = 'Late'
                        endearlyby = 'NA'
                        endedlateby = (act_end0 - sched_end_endmonth0).days
                elif ((ended == False) & (sched_end_text != True)):
                    endedlateby = 'NA'
                    endearlyby = 'NA'
                    if sched_end_endmonth0 >= today:
                        end_status = 'Not due'
                        endedoverdueby = 'NA'
                        endduein = (sched_end_endmonth0 - today).days
                    elif sched_end_endmonth0 < today:
                        end_status = 'Overdue'
                        endduein = 'NA'
                        endedoverdueby = (today - sched_end_endmonth0).days
                elif ((ended == True) & (sched_end_text == True)):
                    endearlyby = 'NA'
                    endedoverdueby = 'NA'
                    endedlateby = 'NA'
                    endduein = 'NA'
                elif ((ended == False) & (sched_end_text == True)):
                    endearlyby = 'NA'
                    endedoverdueby = 'NA'
                    endedlateby = 'NA'
                    endduein = 'NA'

                # calculate actual duration and compare to scheduled
                if ((started == True) & (ended == True) & (sched_start_text == False)):
                    act_duration = (act_end0 - act_start0).days + 1
                    duration_sofar = 'NA'
                elif ((started == True) & (ended == False) & (sched_start_text == False)):
                    act_duration = 'NA'
                    duration_sofar = (today - act_start0).days + 1
                else:
                    act_duration = 'NA'
                    duration_sofar = 'NA'

                if ((sched_duration != 'NA') & (duration_sofar != 'NA')):
                    delta_duration = (duration_sofar - sched_duration)
                    # positive number means action overran the scheduled length
                elif ((sched_duration != 'NA') & (act_duration != 'NA')):
                    delta_duration = (act_duration - sched_duration)
                    # positive number means action overran the scheduled length
                else:
                    delta_duration = 'NA'

                # Mark those due to start this month and in next 30 days
                if ((started == False) & (sched_start_text != 1)):
                    duetostartthismonth = ((sched_start_endmonth0.month == today.month) & (sched_start_endmonth0.year == today.year))
                    duetostartwithin30days = (sched_start_endmonth0 < today - timedelta(days=30))
                else:
                    duetostartthismonth = 'NA'
                    duetostartwithin30days = 'NA'

                if ((sched_start_text != 1)):
                    duetostartlastmonth = ((sched_start_endmonth0.month == today.month - 1) & (sched_start_endmonth0.year == today.year))
                    duetostartinlast30days = (sched_start_endmonth0 < today - timedelta(days=30))
                else:
                    duetostartlastmonth = 'NA'
                    duetostartinlast30days = 'NA'

                # TODO: due to end/ended/due to start/started LAST MONTH
                if ((ended == False) & (sched_end_text != 1)):
                    duetoendthismonth = ((sched_end_endmonth0.month == today.month) & (sched_end_endmonth0.year == today.year))
                    duetoendwithin30days = (sched_end_endmonth0 < today - timedelta(days=30))
                else:
                    duetoendthismonth = 'NA'
                    duetoendwithin30days = 'NA'

                if ((sched_end_text != 1)):
                    duetoendlastmonth = ((sched_end_endmonth0.month == today.month - 1) & (sched_end_endmonth0.year == today.year))
                    duetoendinlast30days = (sched_end_endmonth0 < today - timedelta(days=30))
                else:
                    duetoendlastmonth = 'NA'
                    duetoendinlast30days = 'NA'

                # Mark those started or ended this month and in last 30 days
                if ((started == True) & (sched_start_text == False)):
                    startedthismonth = ((act_start0.month == today.month) & (sched_start_endmonth0.year == today.year))
                    startedinlast30days = (act_start0 < today - timedelta(days=30))
                else:
                    startedthismonth = 'NA'
                    startedinlast30days = 'NA'

                if ((ended == True) & (sched_end_text == False)):
                    endedthismonth = ((act_end0.month == today.month) & (sched_end_endmonth0.year == today.year))
                    endedinlast30days = (act_end0 < today - timedelta(days=30))
                else:
                    endedthismonth = 'NA'
                    endedinlast30days = 'NA'

                # TODO: but still write the end-of-month dates because of excel

                #===================================================================
                # WRITE PROCESSED RESULT TO CSV
                #===================================================================

                dept_abb = deptdict[dept_name]

                # build row
                row0 = [dept_abb, dept_name, dept_id, dept_url, priority_body, priority_id, priority_strapline, action_id, action_body, \
                       action_notes, schedule_start_date, schedule_end_date, actual_start_date, actual_end_date, subaction_id, \
                       subaction_body, subaction_notes, subaction_schedule_start_date, subaction_schedule_end_date, \
                       act_start, act_end, sched_start_endmonth, sched_end_endmonth, \
                       sched_duration, act_duration, duration_sofar, delta_duration, \
                       started, ended, start_status, end_status, startearlyby, startedlateby, startoverdueby, \
                       endearlyby, endedlateby, endedoverdueby, \
                       duetostartthismonth, duetoendthismonth, duetostartwithin30days, duetoendwithin30days, \
                       duetostartlastmonth, duetoendinlast30days, duetoendlastmonth, duetoendinlast30days, \
                       startedthismonth, startedinlast30days, endedthismonth, endedinlast30days, \
                       carriedover, # add new stuff here - it won't throw off the counting of items in the analytics\
                       subaction_schedule_start_date_orig, subaction_schedule_end_date_orig, \
                       subaction_actual_start_date_orig, subaction_actual_end_date_orig, \
                       datetimestring, datestring]

                # clean output of HMTL tags and entities
                # FIXME: make this cleanup work so it replaces all entities - the unescape solution is not robust

                row = []
                for cell in row0:
                    if isinstance(cell, basestring):
                        t = cell
                        # get rid of HTML coded entities which break R imports
                        cellsoup = BeautifulSoup(cell)
                        text_parts = cellsoup.findAll(text=True)
                        textcell = ' '.join(text_parts)
                        t1 = textcell
                        #t = re.sub(textcell, '\n', '')
                        t0 = t1.replace(' & #39;', '\'').replace('&amp;#39;', '\'').replace('&amp;#40;', '\'').replace('&amp;#41;', '\'')
                        t = t0.replace('\r\n', ' ').replace('\n', ' ')
                        # FIXME: remove newline characters from within the resulting text
                        # TODO: check whether text within tags is not being lost
                    elif isinstance(cell, bool):
                        # replace boolean values with 0/1 for easy averaging in excel
                        if cell == True:
                            t = 1
                        else:
                            t = 0

                    else:
                        t = cell
                    row.append(t)

                # write row
                if writecsv == 1:
                    writer.writerow(row)
                else:
                    print('NOTE: no CSV writing done - test run only. See switch at start of script')

                rowDict = dict(zip(header, row0))

                if toscraperwiki == 1:
                    scraperwiki.sqlite.save(unique_keys=['subaction_id', 'datetime'],data=rowDict, table_name='Actions')

                # add row to list of rows if needed for analytics
                if ((analytics == 1) | (timeseriesanalytics == 1)):
                    alldata.append(row0)
if writecsv == 1:
    csvfile.close()
    shutil.copy(csvout, csvout_final)

#===============================================================================
# #===============================================================================
# # ADVANCED ANALYTICS 1: GETTING THE TOP-LEVEL AGGREGATE FIGURES
# #===============================================================================
#===============================================================================

if analytics == 1:
    print "Starting analytics..."
    execfile("./bp_analytics.py")

if timeseriesanalytics != 0:
    print 'Starting analytics'
    execfile("bp_timeseries.py")

# TODO: build log of what was downloaded/calculated from where and when    
