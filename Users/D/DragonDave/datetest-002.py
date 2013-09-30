import scraperwiki
import datetime
import dateutil.parser

"""Set something up to happen after a certain time each day."""

# Blank Python
now=datetime.datetime.now()


def save_trigger_time(time=datetime.time(8,0)):
    if time < now.time():
        trigger = now+datetime.timedelta(days=1)
    else:
        trigger = now

    fulltrigger=datetime.datetime.combine(trigger, time)

    scraperwiki.sqlite.save_var('trigger', fulltrigger.isoformat())

def check_trigger():
    rawtrigger=scraperwiki.sqlite.get_var('trigger')
    print "R", rawtrigger
    if not rawtrigger:
        print "X No rawtrigger"
        return True
    trigger=dateutil.parser.parse(rawtrigger)
    print "T", trigger
    return trigger < now
           
check_trigger()
save_trigger_time()
 
import scraperwiki
import datetime
import dateutil.parser

"""Set something up to happen after a certain time each day."""

# Blank Python
now=datetime.datetime.now()


def save_trigger_time(time=datetime.time(8,0)):
    if time < now.time():
        trigger = now+datetime.timedelta(days=1)
    else:
        trigger = now

    fulltrigger=datetime.datetime.combine(trigger, time)

    scraperwiki.sqlite.save_var('trigger', fulltrigger.isoformat())

def check_trigger():
    rawtrigger=scraperwiki.sqlite.get_var('trigger')
    print "R", rawtrigger
    if not rawtrigger:
        print "X No rawtrigger"
        return True
    trigger=dateutil.parser.parse(rawtrigger)
    print "T", trigger
    return trigger < now
           
check_trigger()
save_trigger_time()
 
