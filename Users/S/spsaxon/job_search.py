import scraperwiki
import lxml.html
import re 
import urllib
import dateutil.parser
import datetime

# TODO
# Better checks for when site goes down - setup number of attempts
#
# sometimes scrape fails without having finished 
# check whether page number is past maximum calculated
# and try again if not
#
#


# Query parameters
# tm = <uint> ; today = 0, since yesterday = 1, last two days = 2 ...
# pg = <uint> pagination number
# re = ????
base_url = "https://jobsearch.direct.gov.uk/Jobsearch/PowerSearch.aspx"

def scrape(since_days = 1, page = 1):
    """
    Scrape all the jobs from the site inserted since x days ago starting at page y
    """
    hdr = () # the header names as parsed on first pass
    data = [] # jobs records
    total =0 # total jobs in last x days
    first = True
    scrape_start_time = datetime.datetime.today()
    while True:
        try:
            print "Reading page %d " % page
            query_data = {"pg": page, "tm": since_days}
            url = base_url + "?" + urllib.urlencode(query_data)
            print "... from %s." % url
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
        except URLError as e:
            sleep(5)
            continue

        #Pagination - read only once to avoid creeping total
        if (first):
            pgn_res_div = root.cssselect("div.searchSummary span")
            pgn_res = pgn_res_div[0].text_content() if pgn_res_div else ""
            p = re.compile(r'Jobs ([\d]+)-([\d]+) of ([\d]+)')
            m = p.match(pgn_res)
            if (m):
                start, end, total = m.groups()
            total = int(total)
            print "Reading %d in total..." % total
            first = False

        row_els = root.cssselect("table.JSresults tr") 
        if (len(row_els) > 1):
            #Set headers
            if (not first):
                hdrs = row_els[0].cssselect("th")
                hdr = (hdrs[0].text_content(), hdrs[2].text_content(), hdrs[3].text_content(), hdrs[4].text_content())
                print hdr
            # read job records for this page
            for tr in row_els[1:]:
                tds = tr.cssselect("td")
                if (tds):
                    date, job_title, company, location = dateutil.parser.parse(tds[0].text_content()).date(), tds[2].text_content(), tds[3].text_content(), tds[4].text_content()
                    id = tds[0].cssselect("a")[0].attrib['name']
                    data.append({'id': id, 'date': date, 'job_title': job_title, 'company': company, 'location': location})
        else:
            continue # sometimes the page reads as blank so try again
        if (len(data) > total):
            break # only finish when all the records have been read
        print "Read %d..." % len(data)
        page = page + 1    
    
    scraperwiki.sqlite.save(unique_keys=['id'],data=data,table_name="jobs",verbose=2)
    scrape_data = {'start': scrape_start_time, 'total': total, 'pages': page}
    scraperwiki.sqlite.save(unique_keys=['start'],data=scrape_data,table_name="scrape_data",verbose=2)
    #end def

scrape(1)