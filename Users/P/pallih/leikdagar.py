# Blank Python

import scraperwiki
from icalendar import Calendar, Event
from datetime import datetime
from icalendar import UTC # timezone
from icalendar import vCalAddress, vText


scraperwiki.sqlite.attach('leikdagar-pepsi-deild-karla-2011') 
keys  = scraperwiki.sqlite.execute('select * from `leikdagar_pepsi_deild_karla_2011` limit 0')['keys']
data = scraperwiki.sqlite.select('* from leikdagar_pepsi_deild_karla_2011')
#print data
#print keys

cal = Calendar()

cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')


event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))

#organizer = vCalAddress('MAILTO:noone@example.com'

#organizer.params['cn'] = vText('Max Rasmussen')
#organizer.params['role'] = vText('CHAIR')
#event['organizer'] = organizer
event['location'] = vText('Odense, Denmark')

event['uid'] = '20050115T101010/27346262376@mxm.dk'
event.add('priority', 5)

attendee = vCalAddress('MAILTO:maxm@example.com')
attendee.params['cn'] = vText('Max Rasmussen')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

attendee = vCalAddress('MAILTO:the-dude@example.com')
attendee.params['cn'] = vText('The Dude')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

cal.add_component(event)

print cal


#for row in data:
#    print row
    
    

# Blank Python

import scraperwiki
from icalendar import Calendar, Event
from datetime import datetime
from icalendar import UTC # timezone
from icalendar import vCalAddress, vText


scraperwiki.sqlite.attach('leikdagar-pepsi-deild-karla-2011') 
keys  = scraperwiki.sqlite.execute('select * from `leikdagar_pepsi_deild_karla_2011` limit 0')['keys']
data = scraperwiki.sqlite.select('* from leikdagar_pepsi_deild_karla_2011')
#print data
#print keys

cal = Calendar()

cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')


event = Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=UTC))
event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=UTC))
event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=UTC))

#organizer = vCalAddress('MAILTO:noone@example.com'

#organizer.params['cn'] = vText('Max Rasmussen')
#organizer.params['role'] = vText('CHAIR')
#event['organizer'] = organizer
event['location'] = vText('Odense, Denmark')

event['uid'] = '20050115T101010/27346262376@mxm.dk'
event.add('priority', 5)

attendee = vCalAddress('MAILTO:maxm@example.com')
attendee.params['cn'] = vText('Max Rasmussen')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

attendee = vCalAddress('MAILTO:the-dude@example.com')
attendee.params['cn'] = vText('The Dude')
attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
event.add('attendee', attendee, encode=0)

cal.add_component(event)

print cal


#for row in data:
#    print row
    
    

