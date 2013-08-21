import commands
import scraperwiki



u = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"

def new_scrape(url):
    return commands.getoutput('curl -k --sslv3 "%s"' % url)

print new_scrape(u)import commands
import scraperwiki



u = "https://eservice.pssg.gov.bc.ca/LRA/reporting/public/newregistrations.do?method=get&registrationRole=all&startDate=05%2F14%2F2012&endDate=05%2F14%2F2012"

def new_scrape(url):
    return commands.getoutput('curl -k --sslv3 "%s"' % url)

print new_scrape(u)