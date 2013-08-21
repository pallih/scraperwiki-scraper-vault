import scraperwiki
import time, datetime, csv
import mechanize
from BeautifulSoup import BeautifulSoup

base_url = "http://www.gov.pe.ca/corporations/index.php"
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
header = [('CompanyNumber','CompanyName','IncorporationDate')]
delay = 0.5
show_progress = True
pages_remaining = -1  # set number of pages to scrape, -1 for all

def get_corporations(html):
    corporations = []
    soup = BeautifulSoup(html)
    for row in soup.findAll('table')[1].findAll('tr'):
        cells = row.findAll('td')
        if len(cells)==4 and cells[1].a:
            company_name = str(cells[1].a.contents[0]).strip()
            company_name = company_name.replace('&amp;','&')
            if company_name: # watch out for first Null row
                company_link = base_url + '?' + cells[1].a['href'].split('?')[1] # requires captcha
                company_number = cells[2].a.contents[0]
                t = cells[3].a.contents[0]
                date_scraped = str(datetime.datetime.now())
                registration_date = datetime.date(int(t[-4:]),int(months.index(t[3:6]))+1,int(t[:2]))
                data = { 'CompanyNumber':company_number,
                         'CompanyName':company_name,
                         'IncorporationDate':registration_date,
                         'DateScraped':date_scraped
                        }
                print data
                scraperwiki.sqlite.save(unique_keys=["CompanyNumber"], data=data)
                corporations.append((company_number,company_name,registration_date, date_scraped),)
                #print corporations
    return corporations                

if show_progress:
    print 'processing page 1'

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(base_url)
br.select_form("SearchForm")
all_corporations = []
corporations = get_corporations(br.submit().read())
page_count = 1

while corporations and pages_remaining:
    all_corporations += corporations
    time.sleep(delay)
    pages_remaining -= 1
    if pages_remaining:
        if show_progress:
            page_count += 1
            print 'processing page %s' % page_count
        br.select_form("next")
        corporations = get_corporations(br.submit().read())
      #  scraperwiki.sqlite.save(unique_keys=["CompanyNumber"],data=dict(CompanyNumber=item[0],CompanyName=item[1],IncorporationDate=item[2],DateScraped=item[3]))

#if show_progress:
    #print len(all_corporations),'corporations scraped from all pages'

#for item in all_corporations:
    #scraperwiki.sqlite.save(unique_keys=["CompanyNumber"],data=dict(CompanyNumber=item[0],CompanyName=item[1],IncorporationDate=item[2],DateScraped=item[3]))


