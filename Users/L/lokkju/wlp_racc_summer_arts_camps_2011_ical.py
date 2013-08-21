# Blank Python
sourcescraper = 'wlp_racc_summer_arts_camps_2011'
import scraperwiki,string,base64
from datetime import datetime

t_vcal=string.Template('''
BEGIN:VCALENDAR
PRODID:-//Calendar//Calendar Event//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
DTSTAMP:${DTSTAMP}
  
${EVENTS}

END:VCALENDAR
''')

t_vevent=string.Template('''
BEGIN:VEVENT
DTSTART:${DTSTART}
DTEND:${DTEND}

SUMMARY: ${TITLE}
DESCRIPTION: Summer Arts Camps 2011 - Presented by RACC - ${DESC}
UID:${UID}
LOCATION: RACC
SEQUENCE:0
END:VEVENT
''')

scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select(           
    '''start_date,end_date,link_url,title,updated from swdata'''
)

events = []
for d in data:
    event_text = t_vevent%{'DTSTART':datetime.strftime(d['start_date'],"%Y%m%dT%H%M%S"),
        'DTEND':datetime.strftime(d['end_date'],"%Y%m%dT%H%M%S"),
        'TITLE':d['title'],
        'DESC':d['link_url'],
        'UID':1
    }
    # TODO: Fix UID
    events.append(events_text)

print t_vcal%{'DTSTAMP':datetime.strftime(datetime.now(),"%Y%m%dT%H%M%S"),'EVENTS':"\n".join(events)}
