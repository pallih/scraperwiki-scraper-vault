# this is a scraper of Northamptonshire planning applications for use by Openly Local

# works through 7 short lists and gathers around 15 or so current applications only

import scraperwiki
from datetime import datetime
import sys

scrapemark = scraperwiki.utils.swimport("scrapemark_09")
util = scraperwiki.utils.swimport("utility_library")
base = scraperwiki.utils.swimport("openlylocal_base_scraper")

DEBUG = False

districts = [ 'Corby', 'Daventry', 'East Northamptonshire', 'Kettering', 'Northampton', 'South Northamptonshire', 'Wellingborough' ]

search_url = 'http://www.northamptonshire.gov.uk/en/councilservices/Environ/planning/planapps/Pages/currentapps_details.aspx'

scrape_ids = """
    <h1> Current applications </h1> <div>
    {* <table> 
    <tr> Application Number {{ [records].uid }} </tr>
    <tr> <td> Location </td> <td> {{ [records].address }} </td> </tr>
    <tr> <td> Proposal </td> <td> {{ [records].description }} </td> </tr>
    <tr> <td> Case Officer </td> <td> {{ [records].case_officer }} </td> </tr>
    <tr> <td> Received </td> <td> {{ [records].date_received }} </td> </tr>
    <tr> <td> Valid </td> <td> {{ [records].date_validated }} </td> </tr>
    <tr> <td> Target for Decision </td> <td> {{ [records].target_decision_date }} </td> </tr>
    <tr> <td> Consultation Start </td> <td> {{ [records].consultation_start_date }} </td> </tr>
    <tr> <td> Consultation End </td> <td> {{ [records].consultation_end_date }} </td> </tr>
    <tr> submitted documents for this planning application <a href="{{ [records].url|abs }}" /> </tr>
    </table> *}
    </div>
    """

scraper = base.BaseScraper()
if DEBUG: scraper.DEBUG = True

response = util.open_url(scraper.br, search_url)
html = response.read()
if DEBUG: print html

final_result = []
for d in districts:
    response = scraper.br.follow_link(text=d)
    html = response.read()
    url = response.geturl()
    result = scrapemark.scrape(scrape_ids, html, url)
    if result and result.get('records'):
        for rec in result['records']:
            scraper.clean_record(rec)
            rec['date_scraped'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            rec['start_date'] = rec['date_received']
            rec['district'] = d
        final_result.extend(result['records'])
    scraper.br.back()
    if DEBUG: print d, len(result['records'])

if final_result:
        
    scraperwiki.sqlite.save(unique_keys=['uid'], data=final_result)
    print 'Scraped', len(final_result), 'records'

else:

    print 'No records scraped'

#scraperwiki.sqlite.execute('drop table if exists swvariables')
#scraperwiki.sqlite.commit()


    
    




