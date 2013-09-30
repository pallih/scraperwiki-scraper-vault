import scraperwiki

import datetime
import time
import string

now = datetime.datetime.now()

print now
print now.isoformat()
print now.strftime("%a %b %e %T %z")

import time
import os

def show_zone_info():
    print '\tTZ    :', os.environ.get('TZ', '(not set)')
    print '\ttzname:', time.tzname
    print '\tZone  : %d (%d)' % (time.timezone, (time.timezone / 3600))
    print '\tDST   :', time.daylight
    print '\tTime  :', time.ctime()
    print

print 'Default :'
show_zone_info()

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

print time.strftime("%a %b %e %T %z %Y", time.gmtime())

alphabet = list(string.ascii_lowercase) + list(string.digits) + ['"',"'",'.']

for letter in alphabet:
    record = {}
    record ['letter'] = letter
    record ['done'] = '0'
    print record
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')

letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','z']
count = 1
for letter in letters:

    print letter, count
    count = count+1

import scraperwiki

import datetime
import time
import string

now = datetime.datetime.now()

print now
print now.isoformat()
print now.strftime("%a %b %e %T %z")

import time
import os

def show_zone_info():
    print '\tTZ    :', os.environ.get('TZ', '(not set)')
    print '\ttzname:', time.tzname
    print '\tZone  : %d (%d)' % (time.timezone, (time.timezone / 3600))
    print '\tDST   :', time.daylight
    print '\tTime  :', time.ctime()
    print

print 'Default :'
show_zone_info()

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

print time.strftime("%a %b %e %T %z %Y", time.gmtime())

alphabet = list(string.ascii_lowercase) + list(string.digits) + ['"',"'",'.']

for letter in alphabet:
    record = {}
    record ['letter'] = letter
    record ['done'] = '0'
    print record
#    scraperwiki.sqlite.save(['letter'], data=record, table_name='runtime_info')

letters = ['"', "'", '.','0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','z']
count = 1
for letter in letters:

    print letter, count
    count = count+1

