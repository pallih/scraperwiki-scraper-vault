from scraperwiki import scrape
from scraperwiki.sqlite import save,get_var
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import *

part1 = 'http://www.manta.com/mb?'
part2 = 'search=web+design&refine_company_emp=E01&refine_company_pubpri=private'

urlstrings = [ part1 + str(i) +part2 for i in range(1,2)]

for urlstring in urlstrings:
    page_data=scrape(urlstring)
    #page_data=fromstring(page_data).cssselect('.url')
    print page_datafrom scraperwiki import scrape
from scraperwiki.sqlite import save,get_var
from urllib2 import urlopen
from lxml.html import fromstring
from datetime import *

part1 = 'http://www.manta.com/mb?'
part2 = 'search=web+design&refine_company_emp=E01&refine_company_pubpri=private'

urlstrings = [ part1 + str(i) +part2 for i in range(1,2)]

for urlstring in urlstrings:
    page_data=scrape(urlstring)
    #page_data=fromstring(page_data).cssselect('.url')
    print page_data