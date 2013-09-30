import scraperwiki
from bs4 import BeautifulSoup
import datetime, re


def get_links_per_page(page):
    """
    Extract the company links per page
    """
    url = "http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors?page=" + str(page)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    content = soup.find("div", {"id": "col1_content"})
    companies = content.find_all("div", {"class": "company"})
    base = "http://www.groceryretailonline.com"
    links = [base+x.a['href'] for x in companies]
    return [x for x in links if "BuyersGuide.mvc" in x]


def parse_company_page(url):
    """
    Fetch and parse the company page to extract desired info
    """
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    content = soup.find("div", {"id": "col1_content"})
    date_scraped = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    data = {
        'datescraped': date_scraped,
        'emails': ', '.join(mailsrch.findall(content.text)),
        'company_name': content.span.text,
        'address': content.text.split('\n')[4].strip(),
        'city': content.text.split('\n')[5].strip(),
        'state': content.text.split('\n')[6].strip(),
        'zip': content.text.split('\n')[7].strip(),
        'country': content.text.split('\n')[8].strip(),
        'sourceurl': url
    }
    scraperwiki.sqlite.save(unique_keys=['company_name'], data=data)


def scrape_page(page):
    """
    Execute the scraping per page
    """
    links = get_links_per_page(page)
    for link in links:
        parse_company_page(link)


# Execute sample scrape for page 1
scrape_page(1)






import scraperwiki
from bs4 import BeautifulSoup
import datetime, re


def get_links_per_page(page):
    """
    Extract the company links per page
    """
    url = "http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors?page=" + str(page)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    content = soup.find("div", {"id": "col1_content"})
    companies = content.find_all("div", {"class": "company"})
    base = "http://www.groceryretailonline.com"
    links = [base+x.a['href'] for x in companies]
    return [x for x in links if "BuyersGuide.mvc" in x]


def parse_company_page(url):
    """
    Fetch and parse the company page to extract desired info
    """
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    content = soup.find("div", {"id": "col1_content"})
    date_scraped = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
    mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    data = {
        'datescraped': date_scraped,
        'emails': ', '.join(mailsrch.findall(content.text)),
        'company_name': content.span.text,
        'address': content.text.split('\n')[4].strip(),
        'city': content.text.split('\n')[5].strip(),
        'state': content.text.split('\n')[6].strip(),
        'zip': content.text.split('\n')[7].strip(),
        'country': content.text.split('\n')[8].strip(),
        'sourceurl': url
    }
    scraperwiki.sqlite.save(unique_keys=['company_name'], data=data)


def scrape_page(page):
    """
    Execute the scraping per page
    """
    links = get_links_per_page(page)
    for link in links:
        parse_company_page(link)


# Execute sample scrape for page 1
scrape_page(1)






