import scraperwiki
from datetime import date

# London Planning Applications

util = scraperwiki.utils.swimport("utility_library")

REGION = 'London'
DB_START = 65 # default date (in YYYY-MM-DD format) to scrape from (or a number if you want it to start x days ago)
DB_END = 10 # default date (in YYYY-MM-DD format) to scrape to (or a number if you want it to stop x days ago)
MAX_PER_SESSION = 100 # maximum records to get in one go from one authority
TIMEOUT = 240


# split the authorities into 3 tranches and do one third each time
def daily_schedule(day_num = -1):
    if day_num < 0:
        day_num = date.today().weekday()
    if day_num >= 6:
        util.do_cleanup()
        return
    day_num = day_num % 3
    auth_list = util.get_auths(REGION)
    count = 0
    for auth in auth_list:
        if count % 3 == day_num:
            util.gather_applications(auth, DB_START, DB_END, MAX_PER_SESSION, TIMEOUT)
        count += 1
    print "Completed daily update for "+date.today().strftime('%A')

            
# uncomment this to refresh the authorities list completely
# this is the nuclear option which means all data gets gathered again from DB_START
#scraperwiki.sqlite.execute("drop table if exists authorities")
#scraperwiki.sqlite.commit()

# uncomment this to start again on any single authority
#util.restart_authority('Richmond')

#uncomment these lines to to do a short test scrape on one authority
#auth_list = util.get_auths(['Barnet']) # NB simple string is a region, list is a list of authorities
#for auth in auth_list:
#    util.gather_applications(auth, DB_START, DB_END, 50, 240)

# uncomment this to activate the daily scraping schedule
daily_schedule()

# show table types
#tables = scraperwiki.sqlite.show_tables()
#print tables['authorities']
#print tables['applications']
#info = scraperwiki.sqlite.table_info(name="applications")
#for column in info:
#    print column['name'], column['type']



