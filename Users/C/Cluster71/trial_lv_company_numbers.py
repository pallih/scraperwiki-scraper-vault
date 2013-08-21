# Blank Python

import scraperwiki, math, re, string
from BeautifulSoup import BeautifulSoup as Soup
from urllib import urlopen

search_url = "https://www.lursoft.lv/lapsaext?act=URCP&general=%s&tablepage=%d"
search_chars = string.ascii_lowercase + string.digits

#'pamatdati' is Latvian for basic, finds link to the page with basic company info. 
url_re = re.compile('pamatdati')
digits_re = re.compile('\d+')
date_re = re.compile('\d{2}\.\d{2}\.\d{4}')

def scrape_results(results_table):
    for link in results_table.findAll("a", href=url_re):
        print(link['href'])
        soup = Soup(urlopen(link['href']).read())
        table = soup.find("table", "info")
        print(table)
        if not table:
            continue

        rows = table.findAll('tr')
        print(rows[0].findAll('td')[1].text)

        data = {
            "CompanyName": rows[0].findAll('td')[1].text,
            "EntityType": rows[1].findAll('td')[1].text,
            'RegistryUrl': link['href']
        }

        #If the 5th row contains a date it is the companies liquidation date, 
        #For active companies the row is missing and subsequent rows are shifted up by one
        print(rows[4].findAll('td')[1].text, rows[7].findAll('td')[1].text, rows[8].findAll('td')[1].text)
        if date_re.match(rows[4].findAll('td')[1].text):
            data['Status'] = "Liquidated"
            company_num = rows[8].findAll('td')[1].text
        else:
            data['Status'] = "Active"
            company_num = rows[7].findAll('td')[1].text

        data['CompanyNumber'] = int(digits_re.match(company_num).group())

        scraperwiki.sqlite.save(["CompanyNumber"], data)

def get_results_table(prefix, page_num):
    response = urlopen(search_url % (prefix, page_num))
    soup = Soup(response.read(), convertEntities=Soup.HTML_ENTITIES)
    results_table = soup.find("table", "table")
    return results_table


def scrape_search(prefix):
    curr_page = scraperwiki.sqlite.get_var('curr_page', False)
    num_pages = scraperwiki.sqlite.get_var('num_pages', False)
    
    if curr_page == False:
        print("new prefix, retrieving page count")
        results_table = get_results_table(prefix, 1)
    
        if not results_table:
            return

        num_records = int(results_table.find("td").text[6:])
        num_pages = int(math.floor((num_records-1) / 10))
        curr_page = 1
        scrape_results(results_table)
    else:
        print("Continue scraping %s" % prefix)

    scraperwiki.sqlite.save_var('num_pages', num_pages)
    scraperwiki.sqlite.save_var('curr_page', curr_page)

    for page_num in range(curr_page, num_pages + 1):
        results_table = get_results_table(prefix, page_num)
        scrape_results(results_table)
        scraperwiki.sqlite.save_var('curr_page', page_num)
    
    scraperwiki.sqlite.save_var('num_pages', False)
    scraperwiki.sqlite.save_var('curr_page', False)
    


#Generate all permutations, with repetition, can start from any possible permutation.
def permutations_from(chrs, num, start=False):
    if start == False:
        index = 0
    else:
        index = chrs.index(start[0])

    if num <= 1:
        for c in chrs[index:]:
            yield c
    else:
        for c in chrs[index:]:
            for p in permutations_from(chrs, num - 1, start[1:] if start and c == start[0] else False):
                yield c + p

#Start scrape
start_prefix = scraperwiki.sqlite.get_var('search_prefix', False)

for prefix in permutations_from(search_chars, 2, start_prefix):
    scraperwiki.sqlite.save_var('search_prefix', prefix)
    scrape_search(prefix)
    
scraperwiki.sqlite.save_var('search_prefix', False)