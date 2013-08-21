# To Scrape the PDFs of the OIG's data:
# Scrape multiple pages of reports
# Get the links for all the pdfs
import scraperwiki
import re
import urlparse
import mechanize
from BeautifulSoup import BeautifulSoup
def scrape_pdf_links(starting_url, homepage):
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    links = soup.findAll(href=re.compile('pdf$'))
    for link in links:
        record = {}        
        record['url'] = homepage + link['href']
        record['title'] = link.text
        record['number'] = link['href']
        scraperwiki.sqlite.save(["url"],record)
        print record

#Management Reports
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/editorial_0334.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY10.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY09.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY08.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/gc_1193965173651.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY06.shtm'
page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY05.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/OIG_mgmtrpts_FY04.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/mgmt/Copy_of_editorial_0334.shtm'
#Financial grant reports
#page = 'http://www.dhs.gov/xoig/rpts/audit/editorial_0604.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_10grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_09grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_08grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_07grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_06grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_05grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/editorial_0602.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_04grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_04agrantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_03grantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_03agrantsrpts.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/audit/oig_03bgrantsrpts.shtm'
#Management Advisory Reports
#page = 'http://www.dhs.gov/xoig/rpts/gc_1234544442225.shtm'
#page = 'http://www.dhs.gov/xoig/rpts/advrpt/OIG_FY09_advrpt.shtm'
#Semi-Annual Reports to Congress
#page = 'http://www.dhs.gov/xoig/rpts/semiannl/editorial_0330.shtm'

homepage = 'http://www.dhs.gov'
scrape_pdf_links(page, homepage)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
#next link looks like: http://gao.gov/docsearch/app_processform.php?app_id=docdblite_agency&page=2


