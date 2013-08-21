import mechanize 
import lxml.html
import scraperwiki
import lxml.html
from datetime import date 
#from datetime import datetime
import datetime
import re
record = {}

def scrape_info(info):
    
    #html = scraperwiki.scrape(info)
    root = lxml.html.fromstring(info)
    cells = root.cssselect('ul#results') 
    for cellsInfo in cells:
        detail = cellsInfo.cssselect('li') 
        if detail:
            record['detail'] = "#SOTmentionedyesterday"
            record['link'] = "http://www.parliament.uk/search/advanced"
            #record['ScrapeDate'] = date.today()          
            scraperwiki.sqlite.save(unique_keys=[], data=record)
        
            

parliamenturl = "http://www.parliament.uk/search/advanced"
br = mechanize.Browser()
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(parliamenturl)

#print "All forms:", [ form.name  for form in br.forms() ]

br.select_form(name="aspnetForm")
#print br.form

fullDate = date.today()
#Date = datetime.strptime(fullDate, "%y-%m-%d")
yestDate = fullDate - datetime.timedelta(days=1)
record['date'] = fullDate - datetime.timedelta(days=1)
#print yestDate


splitDate = re.split('\-+', str(yestDate))
day = int(splitDate[1])
month = int(splitDate[2])
#print str(day)

br["ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$txtSearchExact"] = 'stoke-on-trent'
#br["ctl00_ctl00_SiteSpecificPlaceholder_PageContent_AdvancedSearchPanel_ctlFilters_FilterList_ctl06_FilterItem"]=['']
br["ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$ddlDateSearch"] = ["after"]
br["ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$ctlDateFrom$DayList"]  = [str(day)]
br["ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$ctlDateFrom$MonthList"] = [str(month)]
br["ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$ctlDateFrom$YearList"] = [splitDate[0]]


info = br.submit(name='ctl00$ctl00$SiteSpecificPlaceholder$PageContent$AdvancedSearchPanel$btnSearch').read()
#print info

scrape_info(info)


