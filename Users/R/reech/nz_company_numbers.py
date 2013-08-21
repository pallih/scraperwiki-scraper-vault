###############################################################################
#
# Initial Stab at http://www.business.govt.nz/companies/
# Earliest registration: 28 Jul 1862
# 
###############################################################################

import scraperwiki
import lxml.etree
import lxml.html
from datetime import datetime, timedelta
import time
import re
import sys
import string

base_url = 'http://www.business.govt.nz/companies/app/ui/pages/companies/'

def main():

    scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')
    """
    1800-1930 - annually
    1930-1950 - monthly
    1950-1970 - weekly
    1970 + - daily
    """
    print 'Starting at %s ' % (scrape_date,)
    # 
    today = datetime.now()
    today_str = today.strftime('%d/%m/%Y')
    
    while datetime.strptime(scrape_date,'%d/%m/%Y') < datetime.strptime(today_str, '%d/%m/%Y'):
        
        #Chunk up into bite-sized portions
        if datetime.strptime(scrape_date,'%d/%m/%Y') < datetime.strptime('01/01/1930','%d/%m/%Y'):
            print 'scraping annually'
            dates_to_scrape = date_gen(datetime.strptime(scrape_date,'%d/%m/%Y'), 
            datetime.strptime('01/01/1930','%d/%m/%Y'), 365)
            scrape_dates(dates_to_scrape, scrape_date)
            scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')

        elif datetime.strptime(scrape_date,'%d/%m/%Y') < datetime.strptime('01/01/1950','%d/%m/%Y'):
            print 'scraping monthly'
            dates_to_scrape = date_gen(datetime.strptime(scrape_date,'%d/%m/%Y'), 
            datetime.strptime('01/01/1950','%d/%m/%Y'), 30)
            scrape_dates(dates_to_scrape, scrape_date)
            scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')  

        elif datetime.strptime(scrape_date,'%d/%m/%Y') < datetime.strptime('01/01/1970','%d/%m/%Y'):
            print 'scraping bi-Weekly'
            dates_to_scrape = date_gen(datetime.strptime(scrape_date,'%d/%m/%Y'), 
            datetime.strptime('01/01/1970','%d/%m/%Y'), 14)
            scrape_dates(dates_to_scrape, scrape_date)
            scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')  

        elif datetime.strptime(scrape_date,'%d/%m/%Y') < datetime.strptime('01/01/1990','%d/%m/%Y'):
            print 'scraping tri-Daily'
            dates_to_scrape = date_gen(datetime.strptime(scrape_date,'%d/%m/%Y'), 
            datetime.strptime('01/01/1990','%d/%m/%Y'), 4)
            scrape_dates(dates_to_scrape, scrape_date)
            scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')

        elif datetime.strptime(scrape_date,'%d/%m/%Y') >= datetime.strptime('01/01/2000','%d/%m/%Y'):
            print 'scraping Daily'
            dates_to_scrape = date_gen(datetime.strptime(scrape_date,'%d/%m/%Y'), today, 1)
            scrape_dates(dates_to_scrape, scrape_date)
            scrape_date = scraperwiki.sqlite.get_var('last_date', default='27/07/1862')
    
    
    # Default to today
    scraperwiki.sqlite.save_var('last_date', today_str)



def scrape_dates(dates_to_scrape, fd):

    first_date = datetime.strptime(fd,'%d/%m/%Y')
    print 'Starting from: ' + str(first_date)
    for from_date, to_date in dates_to_scrape:
        # build URL
        day_url = ('search?start=0&limit=200&incorpFrom=%s&incorpTo=%s&mode=advanced') % (from_date, to_date)
        
        # Work around slow responses
        try:
            page = scraperwiki.scrape(base_url + day_url)
        except:
            print 'sleeping...'
            time.sleep(12)
            page = scraperwiki.scrape(base_url + day_url)

        print  'Scraping : ' + base_url + day_url
        parsed_page = lxml.html.fromstring(page)
        num = parsed_page.cssselect("div .totalInfo h4")
    
        if num:
            # If there are over 200 results we will have to reverse the result list and then start from
            # there - this is a nasty style hard limit - so let's hope we don't ever get over 400 results
            num = re.match('.*of (.*) results.', num[0].text).groups()[0]
            print 'Scraping ' + str(num) + ' recs..'

            if int(num) > 400:
                ## Attempt Alpha filter scraping
                for a in string.lowercase:
                    a_url = day_url + '&q=%s' % (a,)
                    alpha_url = base_url + a_url
                    page = scraperwiki.scrape(alpha_url)
                    print 'Scraping alpha: ' + alpha_url
                    parsed_page = lxml.html.fromstring(page)
                    res = parsed_page.cssselect("div .totalInfo h4")
                    if res:
                        scrape_list(parsed_page, alpha_url)
                    else:
                        print 'No Alpha match'
                        continue
            else:
                reverse = int(num) - 200 if int(num) > 200 else  False
                scrape_list(parsed_page, day_url, reverse, reverse)

        else:
            print 'No match..'
                
        #save
        scraperwiki.sqlite.save_var('last_date', to_date)
        

def scrape_list(page, url, reverse=False, reverse_num=False):
    
    ldata = [ ]
    rows = page.cssselect('tr')[7:-1] # remove rows with no links

    if reverse_num and not reverse:
        rows  = rows[0:int(reverse_num)]

    for row in rows:
        link = row.cssselect('a.link') # links inidicate valid records
        data = {}

        if link:
            inc_date = datetime.strptime(row.cssselect('.incorporationDate label')[0].text.strip(),'%d %b %Y')
            
            try:
                data['companyIncorporated'] = datetime.strftime(inc_date, '%Y-%m-%d')
            except:
                data['companyIncorporated'] = ('%d-%d-%d') % (inc_date.year, inc_date.month, inc_date.day)
    
            data['companyType'] = row.cssselect('.entityType')[0].text_content().strip()
            data['companyName'] = row.cssselect('.entityName')[0].text_content().strip()
            company_info = row.cssselect('.entityInfo')[0].text_content().strip()
            data['companyNumber'] , data['companyStatus']  = re.match('\(([0-9]*)\)(.*)'+str(data['companyType'])+'.*$', company_info).groups()
            data['companyRegisteredAddress']  = row.cssselect('td div div')[0].text_content().strip()
            data['companyRegistrationUrl']  = base_url + data['companyNumber'] + '/detail'
            data['date_scraped'] =  time.time()
            ldata.append(data)

        # save a batch at a time
        scraperwiki.sqlite.save(unique_keys=['companyNumber',], data=ldata)
            
    if reverse:
        print 'Reversing..'
        # scrape reversed list - anything with over 200 results
        url += '&sf=entityName&sd=desc'
        reverse_url = base_url + url
        page = scraperwiki.scrape(reverse_url)
        parsed_page = lxml.html.fromstring(page)
        # Scrape the reversed list, sending number of rows to scrape
        scrape_list(parsed_page, url, False, reverse_num)
        
    
def date_gen(from_date=None, end_date=datetime.now(), delta_days=1):
    
    delta=timedelta(days=delta_days)
    daydelta=timedelta(days=1)

    to_date = from_date + delta - daydelta
    
    while from_date <= end_date:
        yield [('%d/%d/%d') % (from_date.day, from_date.month, from_date.year),
        ('%d/%d/%d') % (to_date.day, to_date.month, to_date.year),]
        
        from_date = to_date + daydelta
        to_date = from_date + delta - daydelta

    return

main()