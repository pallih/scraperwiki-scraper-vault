import scraperwiki
import re
from datetime import date

# River Thames planning applications

pa_lib = scraperwiki.utils.swimport("pa_scraper_library")

AUTHORITIES = ['richmond','elmbridge']
REGION = 'London'
DB_START = 28 # default date (in YYYY-MM-DD format) to scrape from (or a number if you want it to start x days ago)
DB_END = 0 # default date (in YYYY-MM-DD format) to scrape to (or a number if you want it to stop x days ago)
MAX_PER_SESSION = 100 # maximum records to get in one go from one authority
TIMEOUT = 240
NUM_PER_DAY = 10

def daily_schedule(day_num = -1):
    if day_num < 0:
        day_num = date.today().weekday()
    if day_num >= 6: # on Sunday
        pa_lib.do_cleanup()
        return
    auth_list = pa_lib.get_auths(AUTHORITIES)
    auth_list = sorted(auth_list, cmp=lambda x,y: cmp(x.get('last_date'),y.get('last_date'))) # sort by most recent application date
    for i in range(0, min(NUM_PER_DAY, len(auth_list))):
        pa_lib.gather_applications(auth_list[i], DB_START, DB_END, MAX_PER_SESSION, TIMEOUT)
    print "Completed daily update for "+date.today().strftime('%A')


def hydro_applications(schema, aname):
    data = scraperwiki.sqlite.select("* FROM applications " #authority='"+aname+"'"+
                                     +"WHERE (description LIKE '%hydro%' OR description LIKE '%turbine%')")
    print "Found",data.__len__()," rows"
    excludes = re.compile("(hydrogen)|(hydrotherapy)|(hydrological)|(hydrogeological)|"
                         +"(hydrocarbon)|(hydrology)|(hydrolysis)|(biomass)|"
                         +"(gas.*turbine)|(mast.*turbine)|(turbine.*mast)|(wind.*turbine)|(turbine.*tower)", re.I)
    for row in data:
        if (excludes.search(row['description']) == None):
            print "Match:",row['authority'],row['reference'],row['description']


# show table types
def debug_tables(schema):
    tables = scraperwiki.sqlite.show_tables(schema)
    print schema+" contains ",tables.__len__()," tables"
    for  table in tables:
        debug_table(table)
    
    #debug_table('authorities')
    #debug_table('swdata') 
    #debug_table('applications') 


def debug_table(tname = 'unknown'):
    num = scraperwiki.sqlite.select("count(*) AS n FROM "+tname)
    print "Table: "+tname+" contains "+str(num[0]['n'])+" rows."
    #info = scraperwiki.sqlite.table_info(name=tname)
    #for column in info:
        #print column['name'], "=>", column['type']


# do a test on one region
def test_region(region, alias):
    scraperwiki.sqlite.attach(region, alias)
    debug_tables(alias)
    hydro_applications(alias, '')

         

# uncomment this to start again on any single authority
#pa_lib.restart_authority('Epping Forest')
# uncomment this to clear any single authority
#pa_lib.remove_authority('Epping Forest')

#uncomment these lines to to do a short test scrape on one authority
#test_authority('elmbridge')

# uncomment this to activate the daily scraping schedule
# daily_schedule()

#test_region('london_planning_applications')
#test_region('south_east_planning_applications')
test_region('east_england_planning_applications', "eepa")
test_region('south_west_planning_applications', "swpa")

