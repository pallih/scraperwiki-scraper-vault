import scraperwiki
import lxml.html
import re 
import urllib


# Query parameters
# tm = <uint> ; today = 0, since yesteday = 1, last two days = 2 ...
# pg = <uint> pagination number
# re = ????
base_url = "https://jobsearch.direct.gov.uk/Jobsearch/PowerSearch.aspx"

def scrape(since_days = 0):
    reading = True
    hdr = ()
    page = 1
    data = []
    n = 0
    while reading:
        print "Reading page %d " % page
        query_data = {"pg": page, "tm": since_days}
        url = base_url + "?" + urllib.urlencode(query_data)
        print "... from %s." % url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        #Pagination
        pgn_res_div = root.cssselect("div.searchSummary span")
        print pgn_res_div
        pgn_res = pgn_res_div[0].text_content() if pgn_res_div else ""
        p = re.compile(r'Jobs ([\d]+)-([\d]+) of ([\d]+)')
        m = p.match(pgn_res)
        if (m and (not n)):
            start, end, total = m.groups()
            n, r = divmod(int(total), (int(end) - int(start)) - 1)

        row_els = root.cssselect("table.JSresults tr") 
        if (len(row_els) > 1):
            print "Reading from %s to %s out of %s ..." % (start, end, total)
            #Set headers
            if (not hdr):
                hdrs = row_els[0].cssselect("th")
                hdr = (hdrs[0].text_content(), hdrs[2].text_content(), hdrs[3].text_content(), hdrs[4].text_content())
                print hdr
            # read job records for this page
            for tr in row_els[1:]:
                tds = tr.cssselect("td")
                if (tds):
                    date, job_title, company, location = tds[0].text_content(), tds[2].text_content(), tds[3].text_content(), tds[4].text_content()
                    id = tds[0].cssselect("a")[0].attrib['name']
                    # print id, date, job_title, company, location
                    # TODO : parse dates as python dates and save in db as well (see docs)
                    data.append({'id': id, 'date': date, 'job_title': job_title, 'company': company, 'location': location})
        else:
            # TODO sometimes scrape fails without having finished 
            # check whether page number is past maximum caluculated
            # and try again if not
            reading = False;
        page = page + 1    
    
    scraperwiki.sqlite.save(unique_keys=['id'],data=data,table_name="jobs",verbose=2)
    scraperwiki.sqlite.save_var('last_page', page)
    #end def

scrape()