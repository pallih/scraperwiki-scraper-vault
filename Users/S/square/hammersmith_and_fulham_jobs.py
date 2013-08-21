import scraperwiki
import urllib
import urllib2
import httplib2
import re
from datetime import datetime
from lxml.html import tostring, fromstring, submit_form

base_url = "https://lboafli.webitrent.com/lboafli_webrecruitment/wrd/run/"
http = httplib2.Http(disable_ssl_certificate_validation=True)

def get_job_details(url, referer):
    print 'Getting job details for', base_url + url
    headers = {
        'Content-type': 'application/x-www-form-urlencoded', 
        'Referer': referer,
        'connection': 'close'}
    response, content = http.request(base_url + url, 'GET', headers=headers)
    
    page = fromstring(content.decode('utf-8'))
    trs = page.cssselect("div#entity > table > tbody > tr")
    id = trs[0].cssselect("th > input[name='VACANCY_ID.TVACANCYUSP.TRENT_REC.1-1-1']")[0].attrib['value']
    title = ' '.join(trs[1].cssselect("td")[1].text_content().split())
    reference = trs[2].cssselect("td")[1].text_content()
    str_date_posted = trs[3].cssselect("td")[1].text_content().strip()
    date_posted = ''
    if (str_date_posted != ''):
        date_posted = datetime.strptime(str_date_posted, '%d/%m/%Y')
    str_closing_date = trs[4].cssselect("td")[1].text_content().strip()
    closing_date = ''
    if (str_closing_date != ''):
        closing_date = datetime.strptime(str_closing_date, '%d/%m/%Y')
    location = ' '.join(trs[5].cssselect("td")[1].text_content().split())
    salary = ' '.join(trs[6].cssselect("td")[1].text_content().split())
    package = ' '.join(trs[7].cssselect("td")[1].text_content().split())
    category = ' '.join(trs[8].cssselect("td")[1].text_content().split())
    description = ' '.join(trs[9].cssselect("td")[1].text_content().split())

    print id, title, reference, date_posted, closing_date, location, salary, package, category, description
    data = {
        'id' : id,
        'title' : title,
        'reference' : reference,
        'date_posted' : date_posted,
        'closing_date' : closing_date,
        'location' : location,
        'salary' : salary,
        'package' : package,
        'category' : category,
        'category' : category,
        'description' : description,
        'date_scraped' : datetime.now(),
        'link' : 'https://lboafli.webitrent.com/lboafli_webrecruitment/wrd/run/ETREC107GF.open?VACANCY_ID=' + id + '&WVID=52561500BT&LANG=USA'
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
def get_jobs(referer, page):
    result_info = page.cssselect("table#searchTable > tr")[1].text_content().strip()
    print "Result information is '" + result_info + "'"
    links = page.cssselect("div#wr_content table > tr > td > table h2 a")
    print 'Found ' + str(len(links)) + ' links on page ' + referer + ', getting job details'
    detail_page_urls = []
    for link in links:
        get_job_details(link.attrib['href'], referer)

    print 'Finished page, checking for next button'
    next_button = page.cssselect("input[name='BU_NEXT.FRM_BUTTON.ET_BASE.1-1-1']")
    if len(next_button) == 0:
        print 'No next button found, finishing'
        return

    print 'Next button found, getting next page'
    result_info = result_info.replace(' ', '').replace('Results', '').replace('of', '-').replace('suitablematches', '')
    result_info_array = result_info.split('-')
    from_record = result_info_array[0]
    to_record = result_info_array[1]
    total_records = result_info_array[2]
    print 'Using params from ' + from_record + ' to ' + to_record + ', total ' + total_records
    action = page.cssselect("div#wr_outer form")[0].attrib['action']
    headers = {
        'Content-type': 'application/x-www-form-urlencoded', 
        'Referer': referer,
        'connection': 'close'}
    body = {
        'BU_NEXT.FRM_BUTTON.ET_BASE.1-1-1':'Next',
        'RESULTS_PP.VAC_SRCHUSP.DUMMY.1-1-1':'10', #per page
        'TOTAL_REC.VAC_SRCHUSP.DUMMY.1-1-1':total_records,
        'REC_FROM.VAC_SRCHUSP.DUMMY.1-1-1':from_record,
        'REC_TO.VAC_SRCHUSP.DUMMY.1-1-1':to_record
    }
    response, content = http.request(base_url + action, 'POST', headers=headers, body=urllib.urlencode(body))
    page = fromstring(content.decode('utf-8'))

    get_jobs(base_url + action, page)

def run_itrent_scraper():
    url = base_url + "ETREC106GF.display_srch_all?WVID=52561500BT&LANG=USA"
    html = scraperwiki.scrape(url)
    page = fromstring(html)

    get_jobs(url, page)


def run_workzone_scraper():
    html = scraperwiki.scrape("http://jobs.workzoneonline.co.uk/vacancylist.cfm")
    page = fromstring(html)
    table = page.cssselect('table.datatable')[0]
    
    id = 0
    title = ''
    location = ''
    salary = ''
    hours = ''
    
    for tr in table.cssselect('tr'):
        tds = tr.cssselect('td')
        if len(tds) == 0:
            continue
        if len(tds) == 4:
            id = tds[0].cssselect('a')[0].attrib['name'].replace('v', '')
            reference = id
            title = tds[0].cssselect('a')[1].attrib['href']
            location = tds[1].text_content().strip()
            salary = tds[2].text_content().strip()
            hours = tds[3].text_content().strip()
    
        elif len(tds) == 1:
            description = ' '.join(tds[0].text_content().split())
            link = 'http://jobs.workzoneonline.co.uk/viewvacancies.cfm?ID=' + id
        
            print id, title, location, salary, hours, description, link
            data = {
                'id' : id,
                'title' : title,
                'location' : location,
                'salary' : salary,
                'hours' : hours,
                'description' : description,
                'date_scraped' : datetime.now(),
                'link' : link
            }
            if len(scraperwiki.sqlite.select("NULL FROM swdata WHERE id=" + id)) > 0:
                updatesql = "UPDATE swdata SET title = '" + title + "', location = '" + location + "', salary = '" + salary + "', hours = '" + hours + "', description = '" + description + "', link = '" + link + "' WHERE id=" + id
                scraperwiki.sqlite.execute(updatesql)
                scraperwiki.sqlite.commit()
            else:
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)

run_itrent_scraper()
run_workzone_scraper()


