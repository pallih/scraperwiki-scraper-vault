'''
Created on Aug 4, 2012

@author: petrbouchal
 
Build DB/CSV from government organogram API, one post per line.'''

output = 'scraperwiki' # should be csv, scraperwiki, both, or none

import json
import urllib2
from urllib2 import urlparse
import csv
from datetime import datetime
#from pprint import pprint

import scraperwiki

now = datetime.now()
today = datetime.today()

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')

# build header
fieldnames = ['level', 'label', 'FTE']

# prepare for writing
if ((output == 'csv') | (output == 'both')):
    csvout = "../output/Organograms" + '_' + filedatestring + '.csv'
    csvout_final = '../output/Organograms_current'
    outfile = open(csvout, 'wb')
    writer = csv.DictWriter(outfile, delimiter=',', dialect='excel', fieldnames=fieldnames)


# write header
if ((output == 'csv') | (output == 'both')): writer.writerow(dict((fn, fn) for fn in fieldnames))

# create list of dates and dates in departments
Mar11 = '2011-03-31'
Sep11 = '2011-09-30'
Mar12 = '2012-31-03'

departments = ['dfe']

datestrings = {}
datestrings['dfe'] = [Sep11]
datestrings['dft'] = [Sep11]

def postsjson(origurl, datatype='report'):
    """ Return iterable JSON of posttype got by updating and querying origurl"""
    urlbits = urlparse.urlparse(origurl)
    newpath = urlbits.path.replace('/id/', '/doc/')
    if datatype == 'info':
        post = ''
    elif datatype == 'report':
        post = '/immediate-reports'
    elif datatype == 'allreport':
        post = '/reports-full'
    elif datatype == 'junior':
        post = '/immediate-junior-staff'
    elif datatype == 'stats':
        post = '/statistics'
    urlpost = urlbits.scheme + '://' + urlbits.netloc + '/' + datestring + newpath + post + '.json'
    returnedposts = json.loads(urllib2.urlopen(urlpost).read())
    print urlpost
    return returnedposts

for department in departments:
    for datestring in datestrings[department]:

        # Top level - Perm Sec

        level = 0
        row = {}

        topurl = 'http://reference.data.gov.uk/' + datestring + '/doc/department/' + department + '/top-post.json'
        toppost = json.loads(urllib2.urlopen(topurl).read())

        topurl2 = toppost['result']['items'][0]['_about']
        print topurl2

        print topurl
        topstats = postsjson(topurl2, 'stats')
        topinfo = postsjson(topurl2, 'info')

        row = {}
        row['level'] = level
        row['label'] = topinfo['result']['primaryTopic']['label'][0]
        row['FTE'] = topinfo['result']['primaryTopic']['heldBy'][0]['tenure']['workingTime']
        print row
        if ((output == 'csv') | (output == 'both')): writer.writerow(row)
        if ((output == 'csv') | (output == 'both')): outfile.close()
        if ((output == 'scraperwiki') | (output == 'both')): scraperwiki.sqlite.save(['level', 'label'], row)

        # Get links to people in level 1 - reporting to perm sec

        level = 1
        print 'Level' + str(level)
        reports1 = postsjson(topurl2, 'report')
        juniors1 = postsjson(topurl2, 'junior')

        #Run through junior staff reporting to perm sec

        for post in juniors1['result']['items']:
            juniorpostlabel = post['label'][0]
            row = {}
            row['level'] = level
            row['label'] = juniorpostlabel
            row['FTE'] = ''
            # set up row here from post 
            # write row here
            print juniorpostlabel

        # run through senior people reporting to perm sec - level 1

        for post in reports1['result']['items']:
            posturlbroken = post['_about']
            print post['label'][0]

            info1 = postsjson(posturlbroken, 'info')
            stats1 = postsjson(posturlbroken, 'stats')
            row = {}
            row = {}

            # now level 2

            level = 2
            # set up row here from post and stats1
            # write row here

            juniors2 = postsjson(posturlbroken, 'junior')
            for post in juniors2['result']['items']:
                print post['label'][0]
                row = {}
                row = {}
                # set up row here
                # write row here

            reports2 = postsjson(posturlbroken)

            for post in reports2['result']['items']:
                print post['label'][0]
                posturlbroken = post['_about']

                info2 = postsjson(posturlbroken, 'info')
                stats2 = postsjson(posturlbroken, 'stats')
                print post['label'][0]
                row = {}
                row = {}
                # set up row here from post and stats1
                # write row here

                # retrieve level 3 people

                level = 3

                juniors3 = postsjson(posturlbroken, 'junior')
                for post in juniors3['result']['items']:
                    print post['label'][0]
                    row = {}
                    row = {}
                    # set up row here
                    # write row here

                reports3 = postsjson(posturlbroken)

                for post in reports3['result']['items']:
                    posturlbroken = post['_about']
                    print posturlbroken

                    info3 = postsjson(posturlbroken, 'info')
                    stats3 = postsjson(posturlbroken, 'stats')
                    print post['label'][0]
                    row = {}
                    row = {}
                    # set up row here from post and stats
                    # write row here

                    level = 4

                    juniors4 = postsjson(posturlbroken, 'junior')
                    for post in juniors4['result']['items']:
                        print post['label'][0]
                        row = {}
                        row = {}
                        # set up row here
                        # write row here

                    reports4 = postsjson(posturlbroken)

                    for post in reports4['result']['items']:
                        print post['label'][0]
                        posturlbroken = post['_about']

                        info4 = postsjson(posturlbroken, 'info')
                        stats4 = postsjson(posturlbroken, 'stats')
                        row = {}
                        row = {}
                        # set up row here from post and stats4
                        # write row here

                        juniors5 = postsjson(posturlbroken, 'junior')
                        for post in juniors5:
                            print post['label'][0]
                            row = {}
                            row = {}
                            # set up row here
                            # write row here


'''
Created on Aug 4, 2012

@author: petrbouchal
 
Build DB/CSV from government organogram API, one post per line.'''

output = 'scraperwiki' # should be csv, scraperwiki, both, or none

import json
import urllib2
from urllib2 import urlparse
import csv
from datetime import datetime
#from pprint import pprint

import scraperwiki

now = datetime.now()
today = datetime.today()

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')

# build header
fieldnames = ['level', 'label', 'FTE']

# prepare for writing
if ((output == 'csv') | (output == 'both')):
    csvout = "../output/Organograms" + '_' + filedatestring + '.csv'
    csvout_final = '../output/Organograms_current'
    outfile = open(csvout, 'wb')
    writer = csv.DictWriter(outfile, delimiter=',', dialect='excel', fieldnames=fieldnames)


# write header
if ((output == 'csv') | (output == 'both')): writer.writerow(dict((fn, fn) for fn in fieldnames))

# create list of dates and dates in departments
Mar11 = '2011-03-31'
Sep11 = '2011-09-30'
Mar12 = '2012-31-03'

departments = ['dfe']

datestrings = {}
datestrings['dfe'] = [Sep11]
datestrings['dft'] = [Sep11]

def postsjson(origurl, datatype='report'):
    """ Return iterable JSON of posttype got by updating and querying origurl"""
    urlbits = urlparse.urlparse(origurl)
    newpath = urlbits.path.replace('/id/', '/doc/')
    if datatype == 'info':
        post = ''
    elif datatype == 'report':
        post = '/immediate-reports'
    elif datatype == 'allreport':
        post = '/reports-full'
    elif datatype == 'junior':
        post = '/immediate-junior-staff'
    elif datatype == 'stats':
        post = '/statistics'
    urlpost = urlbits.scheme + '://' + urlbits.netloc + '/' + datestring + newpath + post + '.json'
    returnedposts = json.loads(urllib2.urlopen(urlpost).read())
    print urlpost
    return returnedposts

for department in departments:
    for datestring in datestrings[department]:

        # Top level - Perm Sec

        level = 0
        row = {}

        topurl = 'http://reference.data.gov.uk/' + datestring + '/doc/department/' + department + '/top-post.json'
        toppost = json.loads(urllib2.urlopen(topurl).read())

        topurl2 = toppost['result']['items'][0]['_about']
        print topurl2

        print topurl
        topstats = postsjson(topurl2, 'stats')
        topinfo = postsjson(topurl2, 'info')

        row = {}
        row['level'] = level
        row['label'] = topinfo['result']['primaryTopic']['label'][0]
        row['FTE'] = topinfo['result']['primaryTopic']['heldBy'][0]['tenure']['workingTime']
        print row
        if ((output == 'csv') | (output == 'both')): writer.writerow(row)
        if ((output == 'csv') | (output == 'both')): outfile.close()
        if ((output == 'scraperwiki') | (output == 'both')): scraperwiki.sqlite.save(['level', 'label'], row)

        # Get links to people in level 1 - reporting to perm sec

        level = 1
        print 'Level' + str(level)
        reports1 = postsjson(topurl2, 'report')
        juniors1 = postsjson(topurl2, 'junior')

        #Run through junior staff reporting to perm sec

        for post in juniors1['result']['items']:
            juniorpostlabel = post['label'][0]
            row = {}
            row['level'] = level
            row['label'] = juniorpostlabel
            row['FTE'] = ''
            # set up row here from post 
            # write row here
            print juniorpostlabel

        # run through senior people reporting to perm sec - level 1

        for post in reports1['result']['items']:
            posturlbroken = post['_about']
            print post['label'][0]

            info1 = postsjson(posturlbroken, 'info')
            stats1 = postsjson(posturlbroken, 'stats')
            row = {}
            row = {}

            # now level 2

            level = 2
            # set up row here from post and stats1
            # write row here

            juniors2 = postsjson(posturlbroken, 'junior')
            for post in juniors2['result']['items']:
                print post['label'][0]
                row = {}
                row = {}
                # set up row here
                # write row here

            reports2 = postsjson(posturlbroken)

            for post in reports2['result']['items']:
                print post['label'][0]
                posturlbroken = post['_about']

                info2 = postsjson(posturlbroken, 'info')
                stats2 = postsjson(posturlbroken, 'stats')
                print post['label'][0]
                row = {}
                row = {}
                # set up row here from post and stats1
                # write row here

                # retrieve level 3 people

                level = 3

                juniors3 = postsjson(posturlbroken, 'junior')
                for post in juniors3['result']['items']:
                    print post['label'][0]
                    row = {}
                    row = {}
                    # set up row here
                    # write row here

                reports3 = postsjson(posturlbroken)

                for post in reports3['result']['items']:
                    posturlbroken = post['_about']
                    print posturlbroken

                    info3 = postsjson(posturlbroken, 'info')
                    stats3 = postsjson(posturlbroken, 'stats')
                    print post['label'][0]
                    row = {}
                    row = {}
                    # set up row here from post and stats
                    # write row here

                    level = 4

                    juniors4 = postsjson(posturlbroken, 'junior')
                    for post in juniors4['result']['items']:
                        print post['label'][0]
                        row = {}
                        row = {}
                        # set up row here
                        # write row here

                    reports4 = postsjson(posturlbroken)

                    for post in reports4['result']['items']:
                        print post['label'][0]
                        posturlbroken = post['_about']

                        info4 = postsjson(posturlbroken, 'info')
                        stats4 = postsjson(posturlbroken, 'stats')
                        row = {}
                        row = {}
                        # set up row here from post and stats4
                        # write row here

                        juniors5 = postsjson(posturlbroken, 'junior')
                        for post in juniors5:
                            print post['label'][0]
                            row = {}
                            row = {}
                            # set up row here
                            # write row here


