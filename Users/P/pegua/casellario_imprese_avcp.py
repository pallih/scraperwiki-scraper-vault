import scraperwiki
import lxml.html 

#To load pages from casellario.avcp.it avoid redicteting, append "&Autoframed" to any URL
SUFFIX = "&Autoframed"


SITE = "http://casellario.avcp.it"
ROOT_REGIONS = "http://casellario.avcp.it/SOA/soa3.nsf/54447eb449b98030c1256e7f00342526?OpenForm&Autoframed"

REGION_URLS = []
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Abruzzo?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/basilicata?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Calabria?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Campania?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Emilia?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Friuli?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Lazio?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Liguria?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Lombardia?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/marche?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Molise?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Piemonte?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Puglia?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Sardegna?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Sicilia?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Toscana?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Trentino?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Umbria?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Valledaosta?Openview&Autoframed")
REGION_URLS.append("http://casellario.avcp.it/SOA/soa3.nsf/Veneto?Openview&Autoframed")

TEST_COMPANY_URL = "http://casellario.avcp.it/SOA/soa3.nsf/fca0ec0225084653c1256d1b0010a2d0/c1256dcd0060bc33c1256fd500337035?OpenDocument"



#Get anagraphic information about a company from its URL
def get_company_info(company_url):
    html = scraperwiki.scrape(company_url)
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table.Pippo")
    #the first table is the one containg information about the company
    #cell 1 is the company number (fiscal code)
    #cell 3 the address 
    #cell 5 the name
    #cell 7 the zip code (CAP)
    #cell 11 the city
    #cell 13 the vat number (partita IVA)
    #cell 15 the country
    #cell 17 the Company Type
    info_table = tables[0]
    info = {}
    tds = info_table.cssselect("td")
    info["company_number"] = tds[1].cssselect("font")[0].text
    info["company_address"] = tds[3].cssselect("font")[0].text
    info["company_name"] = tds[5].cssselect("font")[0].text
    info["company_zip"] = tds[7].cssselect("font")[0].text
    info["company_city"] = tds[11].cssselect("font")[0].text
    info["company_vat"] = tds[13].cssselect("font")[0].text
    info["company_country"] = tds[15].cssselect("font")[0].text   
    info["company_type"] = tds[17].cssselect("font")[0].text
    info["company_avcp_url"] = company_url
    return info

#get the total number of companies for a given region
def get_company_number_region(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    divs = root.cssselect("div")
    div = divs[7]
    fonts = div.cssselect("font")
    return int(fonts[1].text)

#get the total number of companies
def get_company_number_total(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    divs = root.cssselect("div")
    div = divs[9]
    bs = div.cssselect("b")
    return int(bs[1].text)
    
#get the urls for companies in a region
def get_companies_urls(region_url):
    companies_urls = set();
    tot_companies = get_company_number_region(region_url)
    print "Total companies from website " + str(tot_companies)
    urls_to_visit = []
    for n in range(1,tot_companies,1000):
        urls_to_visit.append(region_url+"&Start="+str(n))
    for url_to_visit in urls_to_visit:
        html = scraperwiki.scrape(url_to_visit)
        root = lxml.html.fromstring(html)
        tables = root.cssselect("table")
        #the third table is the one with the urls
        table = tables[2]
        anchors = table.cssselect("a")
        for anchor in anchors:
            companies_urls.add(SITE+anchor.get("href"))
    return list(companies_urls)
        
def save_companies_urls():

    for region_url in REGION_URLS:
        print "Scraping URL " + region_url 
        companies_urls = get_companies_urls(region_url)
        print "Obtained urls " + str(len(companies_urls))
        data_urls = [ {"company_url":x} for x in companies_urls ] 
        scraperwiki.sqlite.save(unique_keys=["company_url"], data=data_urls, table_name="company_urls")

def check_companies_numbers():
    tot = 0;
    print "Total companies from main page: " + str(get_company_number_total(ROOT_REGIONS))
    for region_url in REGION_URLS:
        tot = tot + get_company_number_region(region_url)
    print "Total companies summing results from regions: " + str(tot)


urls = scraperwiki.sqlite.select("* from company_urls order by company_url")

#main 
N = 20 #commit after colleting 20 samples

last_page = scraperwiki.sqlite.get_var('last_page')

data = []
for i in range(last_page,len(urls)):
    data.append(get_company_info(urls[i]["company_url"]))
    if( i % N == 0):
        scraperwiki.sqlite.save(["company_number"], data, table_name="company_info")
        data = []
        scraperwiki.sqlite.save_var('last_page', i)        

