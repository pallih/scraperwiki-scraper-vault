import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


voluntary_sectors =  ['/Charity-and-Voluntary-Jobs/sector-28']

private_sectors = ['/Accountancy-Finance-Jobs/sector-1', '/Banking-Financial-services-Insurance-Jobs/sector-2', '/Beauty-Hair-Care-Leisure-Jobs/sector-3', '/Childcare-Social-Work-Jobs/sector-4', '/Construction-Architecture-Jobs/sector-5', '/Customer-Service-Call-Centre-Jobs/sector-6', '/Education-Training-Jobs/sector-7', '/Engineering-Jobs/sector-8', '/Environmental-Health-Safety-Jobs/sector-9', '/General-Management-Jobs/sector-10', '/Hotel-Catering-Jobs/sector-11', '/Human-Resource-Jobs/sector-12', '/IT-Jobs/sector-13', '/Legal-Jobs/sector-14']

public_sectors = ['/Public-Sector-Jobs/sector-19']

urlroot = "http://www.nijobfinder.co.uk"

def innerText(element):
    if element.text:
        return element.text.replace(',', '').strip()
    else:
        # Assuming each nested element contains only one child
        return innerText(element.getchildren()[0])



def sanatize_salary(salary):
    salary = re.sub("[^\d-]", "", salary)
    salary_range = salary.split('-')

    try:
        if len(salary_range) == 2:
            salary = (int(salary_range[0]) + int(salary_range[1]))/2;
        else:
            salary = salary_range[0]
    except Exception, e:
        return None

    try:
        salary = int(salary)
    except ValueError:
        salary = None

    return salary;


def summed_salary_with_count(root):
    num_parsed = 0
    summed_salary = 0

    # place your cssselection case here and extract the values
    for tr in root.cssselect('div.result-item span.salary'):
        #print list(tr), lxml.etree.tostring(tr)
        salary = sanatize_salary(innerText(tr).strip())
        if salary is not None:
            num_parsed += 1
            summed_salary += salary

    return [summed_salary, num_parsed]


def find_next_button(root):
    # place your cssselection case here and extract the values
    buttons = root.cssselect('li.next a')

    if len(buttons) > 0:
        return buttons[0]
    else:
        return None


def do_it_for_category(sectors):
    category_num_parsed = 0
    category_summed_salary = 0

    for sector in sectors:
        sector_summed_salary, sector_num_parsed = do_it_for_sector(sector)
        category_num_parsed += sector_num_parsed
        category_summed_salary += sector_summed_salary

    return [category_summed_salary, category_num_parsed]


def do_it_for_sector(sector):
    sector_num_parsed = 0
    sector_summed_salary = 0

    url = urlroot + sector

    # Sorry, I'm tired - if the url is longer than 0 chars then continue
    while len(url) > 0:
        root = lxml.html.parse(url).getroot()

        summed_salary, num_parsed = summed_salary_with_count(root)

        sector_num_parsed += num_parsed
        sector_summed_salary += summed_salary

        next_button = find_next_button(root)
        #print lxml.etree.tostring(next_button)

        if next_button is None:
            url = '' # Wow! How hacky!
        else:
            url = urlroot + next_button.get('href')

    return [sector_summed_salary, sector_num_parsed]


def main():
    summed_private_salary, num_private_parsed = do_it_for_category(private_sectors)
    summed_public_salary, num_public_parsed = do_it_for_category(public_sectors)
    summed_voluntary_salary, num_voluntary_parsed = do_it_for_category(voluntary_sectors)

    avg_private_salary = summed_private_salary / num_private_parsed
    avg_public_salary = summed_public_salary / num_public_parsed
    avg_voluntary_salary = summed_voluntary_salary / num_voluntary_parsed

    # Here is a simple Python dictionary which will go into our datastore
    data = {
       'num_private_parsed' : num_private_parsed,
       'num_public_parsed' : num_public_parsed,
       'num_voluntary_parsed' : num_voluntary_parsed,

       'avg_private_salary' : avg_private_salary,
       'avg_public_salary' : avg_public_salary,
       'avg_voluntary_salary' : avg_voluntary_salary
    }

    # We save the data using the datastore API - it can then be used by a view
    # (in this case http://scraperwiki.com/views/example_shops_view )
    # If a dictionary key is present in unique_keys it means that the value for key will be overwritten
    # every time this scraper is run - otherwise the key will occur twice.
    # In the case I want a overwrite the values for all keys on every scraper run.
    scraperwiki.datastore.save(unique_keys=data.keys(), data=data)

main()import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re


voluntary_sectors =  ['/Charity-and-Voluntary-Jobs/sector-28']

private_sectors = ['/Accountancy-Finance-Jobs/sector-1', '/Banking-Financial-services-Insurance-Jobs/sector-2', '/Beauty-Hair-Care-Leisure-Jobs/sector-3', '/Childcare-Social-Work-Jobs/sector-4', '/Construction-Architecture-Jobs/sector-5', '/Customer-Service-Call-Centre-Jobs/sector-6', '/Education-Training-Jobs/sector-7', '/Engineering-Jobs/sector-8', '/Environmental-Health-Safety-Jobs/sector-9', '/General-Management-Jobs/sector-10', '/Hotel-Catering-Jobs/sector-11', '/Human-Resource-Jobs/sector-12', '/IT-Jobs/sector-13', '/Legal-Jobs/sector-14']

public_sectors = ['/Public-Sector-Jobs/sector-19']

urlroot = "http://www.nijobfinder.co.uk"

def innerText(element):
    if element.text:
        return element.text.replace(',', '').strip()
    else:
        # Assuming each nested element contains only one child
        return innerText(element.getchildren()[0])



def sanatize_salary(salary):
    salary = re.sub("[^\d-]", "", salary)
    salary_range = salary.split('-')

    try:
        if len(salary_range) == 2:
            salary = (int(salary_range[0]) + int(salary_range[1]))/2;
        else:
            salary = salary_range[0]
    except Exception, e:
        return None

    try:
        salary = int(salary)
    except ValueError:
        salary = None

    return salary;


def summed_salary_with_count(root):
    num_parsed = 0
    summed_salary = 0

    # place your cssselection case here and extract the values
    for tr in root.cssselect('div.result-item span.salary'):
        #print list(tr), lxml.etree.tostring(tr)
        salary = sanatize_salary(innerText(tr).strip())
        if salary is not None:
            num_parsed += 1
            summed_salary += salary

    return [summed_salary, num_parsed]


def find_next_button(root):
    # place your cssselection case here and extract the values
    buttons = root.cssselect('li.next a')

    if len(buttons) > 0:
        return buttons[0]
    else:
        return None


def do_it_for_category(sectors):
    category_num_parsed = 0
    category_summed_salary = 0

    for sector in sectors:
        sector_summed_salary, sector_num_parsed = do_it_for_sector(sector)
        category_num_parsed += sector_num_parsed
        category_summed_salary += sector_summed_salary

    return [category_summed_salary, category_num_parsed]


def do_it_for_sector(sector):
    sector_num_parsed = 0
    sector_summed_salary = 0

    url = urlroot + sector

    # Sorry, I'm tired - if the url is longer than 0 chars then continue
    while len(url) > 0:
        root = lxml.html.parse(url).getroot()

        summed_salary, num_parsed = summed_salary_with_count(root)

        sector_num_parsed += num_parsed
        sector_summed_salary += summed_salary

        next_button = find_next_button(root)
        #print lxml.etree.tostring(next_button)

        if next_button is None:
            url = '' # Wow! How hacky!
        else:
            url = urlroot + next_button.get('href')

    return [sector_summed_salary, sector_num_parsed]


def main():
    summed_private_salary, num_private_parsed = do_it_for_category(private_sectors)
    summed_public_salary, num_public_parsed = do_it_for_category(public_sectors)
    summed_voluntary_salary, num_voluntary_parsed = do_it_for_category(voluntary_sectors)

    avg_private_salary = summed_private_salary / num_private_parsed
    avg_public_salary = summed_public_salary / num_public_parsed
    avg_voluntary_salary = summed_voluntary_salary / num_voluntary_parsed

    # Here is a simple Python dictionary which will go into our datastore
    data = {
       'num_private_parsed' : num_private_parsed,
       'num_public_parsed' : num_public_parsed,
       'num_voluntary_parsed' : num_voluntary_parsed,

       'avg_private_salary' : avg_private_salary,
       'avg_public_salary' : avg_public_salary,
       'avg_voluntary_salary' : avg_voluntary_salary
    }

    # We save the data using the datastore API - it can then be used by a view
    # (in this case http://scraperwiki.com/views/example_shops_view )
    # If a dictionary key is present in unique_keys it means that the value for key will be overwritten
    # every time this scraper is run - otherwise the key will occur twice.
    # In the case I want a overwrite the values for all keys on every scraper run.
    scraperwiki.datastore.save(unique_keys=data.keys(), data=data)

main()