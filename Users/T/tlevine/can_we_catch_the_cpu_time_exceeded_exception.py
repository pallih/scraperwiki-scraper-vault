from time import time,sleep
from scraperwiki.sqlite import save,save_var,get_var

def main():
    foo=get_var('runId')
    runId=1 if foo==None else foo+1
    save_var('runId',runId)
    try:
        nonsense()
    except:
        try:
            nonsense()
        except:
            exceeded(runId)

def nonsense():
    print "---------------------------------------------------------"
    print "Computing nonsense and printing how many seconds each computation takes"
    prevtime=time()
    while True:
        long(812323525)**long(624333)

        currenttime=time()
        print currenttime-prevtime
        prevtime=currenttime

def exceeded(runId):
    print "---------------------------------------------------------"
    print "Wow, we caught the exception."
    print "Printing the current time so we see how long we have"
    start_time=time()
    while True:
        current_time=time()
        time_after_exception=current_time-start_time
        save([],{"time_after_exception":time_after_exception,"time":current_time,"runId":runId})
        long(812323525)**long(624333)
        sleep(1)
