import scraperwiki
util = scraperwiki.utils.swimport("utility_library")

SOURCES = 'https://docs.google.com/spreadsheet/pub?hl=en_GB&key=0Al4N5JeEnLXAdGtyS1ZJTW9nSEIySWRNN3F5RG1DVVE&single=true&gid=0&output=csv'
CONFIGS = 'https://docs.google.com/spreadsheet/pub?hl=en_GB&key=0Al4N5JeEnLXAdG9IR1QxMDFhVE1KSUJ0UVQ4MjQzY0E&single=true&gid=0&output=csv'

def update_sources(source = None):
    if source:
        num_found = util.import_csv(SOURCES, 'authorities', ['name'], [ source ])
    else:
        num_found = util.import_csv(SOURCES, 'authorities', ['name'])
    if num_found == 1:
        print "Successfully updated details of the %s planning authority" % source
    elif num_found > 0:
        print "Successfully updated details of %s planning authorities" % num_found
    elif source:
        print "Cannot update the %s planning authority - not found" % source
    else:
        print "Cannot update the table of planning authorities - none found"

def update_configs(config = None):
    if config:
        num_found = util.import_csv(CONFIGS, 'configurations', ['name'], [ config ])
    else:
        num_found = util.import_csv(CONFIGS, 'configurations', ['name'])
    if num_found == 1:
        print "Successfully updated details of the %s scraper configuration" % config
    elif num_found > 0:
        print "Successfully updated details of %s scraper configurations" % num_found
    elif config:
        print "Cannot update the %s scraper configuration - not found" % config
    else:
        print "Cannot update the table of scraper configurations - none found"

#update_sources('Middlesbrough') 
#update_configs('ASPNET (Redcar)')
update_sources()
update_configs()

