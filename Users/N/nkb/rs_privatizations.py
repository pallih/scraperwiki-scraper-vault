import scraperwiki
import re
import pprint
import math
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# This function applies the regex to the page
def rH(html, expression):
    
    regex = re.compile(expression)
       
    match = regex.findall(html)
        
    name = ""
    
    if match:
        name = match[0][1]
    
    return name

# Finds the DB that we use
scraperwiki.sqlite.attach('rs_privatizations')

# Corrective scraping: Get back all the buyers!
# First, get the records that don't have a buyer
firm_ids = scraperwiki.sqlite.execute('SELECT id FROM `rs_privatizations`.swdata WHERE buyer = "" AND status = "Sold"')

for firm_id in firm_ids['data']:

    url = "http://www.priv.rs/Privatization+Agency+/80/A.shtml/seo=/companyid=" + str(firm_id[0]) + "/lang_type=eng"
    
    html = scraperwiki.scrape(url)
    
    name = rH(html, '<li class="(title)"><h1>(.*?) <span>| Stara Pazova<\/span><\/h1><\/li>')
    status = rH(html, '<h2>(General Information)</h2>[^\n]\s*<h5>- (.*?)<\/h5>')
    id_nummer = rH(html, '<li class="name">(Identification Number)<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
    method = rH(html, '<li class="name">(Method)<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
    date = rH(html, '<li class="name">(Date)</li>[^\n]\s*<li class="value">(.*?)</li>')
    foundation_year = rH(html, '<li class="name">(Foundation Year)</li>[^\n]\s*<li class="value">(.*?)</li>')
    capital_on_sale = rH(html, '<li class="name">(Capital being offered for sale)</li>[^\n]\s*<li class="value">(.*?)</li>')
    share_of_total_capital = rH(html, '<li class="name">(% of total capital)</li>[^\n]\s*<li class="value">(.*?)</li>')
    nb_employees = rH(html, '<li class="name">(Number of Employees)</li>[^\n]\s*<li class="value">(.*?)</li>')
    nb_employees_with_degree = rH(html, '<li class="name">(Number of employees with university degree)</li>[^\n]\s*<li class="value">(.*?)</li>')
    address = rH(html, '<li class="name">(Address)</li>[^\n]\s*<li class="value">(.*?)</li>')
    town = rH(html, '<li class="name">(Town)</li>[^\n]\s*<li class="value">(.*?)</li>')
    director = rH(html, '<li class="name">(Director)</li>[^\n]\s*<li class="value">(.*?)</li>')
    contact = rH(html, '<li class="name">(Contact Person)</li>[^\n]\s*<li class="value">(.*?)</li>')
    surface_for_devt = rH(html, '<td>(Land for development/Construction)</td>[^\n]\s*<td class="center">(.*?)</td>')
    surface_agri = rH(html, '<td>(Agricultural land)</td>[^\n]\s*<td class="center">(.*?)</td>')
    surface_building = rH(html, '<td>(Total surface of all buildings)</td>[^\n]\s*<td class="center">(.*?)</td>')
    year_of_reference = rH(html, '<tr class="(head)">[^\n]\s*<td>&nbsp;</td><td>.*?</td><td>(.*?)</td></tr>')
    assets = rH(html, '<td>(Ukupna aktiva)</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
    profits = rH(html, '<td>(Neto dobitak gubitak)</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
    date_calls = rH(html, '<td class="w160">(Datum javnog poziva)</td>[^\n]\s*<td class="w200">(.*?)</td>')

    buyer = rH(html, '<td class=\"w\d{3}\">(Fizičko|Pravno) lice<\/td>[^\n]\s*<td class="w\d{3}">(.*)<\/td>')
    buyer_city = rH(html, '<td class="w\d\d\d">(Sedište)</td>[^\n]\s*<td class="w\d\d\d">(.*)</td>')
    buying_price = rH(html, '<td class="w\d\d\d">(Prodajna cena|Krajnja ponuda)</td>[^\n]\s*<td class="w\d\d\d">(.*)</td>')
    date_sale = rH(html, '<td class="w\d{3}">(Datum potpisivanja ugovora)</td>[^\n]\s*<td class="w\d{3}">(.*)</td>')

    data = {
        'id': str(firm_id[0]),
        'name': name,
        'status': status,
        'id_nummer': id_nummer,
        'method': method,
        'date': date,
        'foundation_year': foundation_year,
        'capital_on_sale': capital_on_sale,
        'share_of_total_capital': share_of_total_capital,
        'nb_employees': nb_employees,
        'nb_employees_with_degree': nb_employees_with_degree,
        'address': address,
        'town': town,
        'director': director,
        'contact': contact,
        'surface_for_devt': surface_for_devt,
        'surface_agri': surface_agri,
        'surface_building': surface_building,
        'year_of_reference': year_of_reference,
        'assets': assets,
        'profits': profits,
        'buyer': buyer,
        'buyer_city': buyer_city,
        'buying_price': buying_price,
        'date_calls': date_calls,
        'date_sale': date_sale
    }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# Top value for a company ID. Set at zero so that no job is done
max_id = 0

# Find how many records are in the DB already
num_rows = scraperwiki.sqlite.execute('SELECT COALESCE(MAX(id)+1, 0) FROM `rs_privatizations`.swdata')

#extracts the number of records in the DB
start = num_rows['data'][0][0]
end = start + 1000

if start < max_id:
    
    #Gets down to the actual scraping
    for x in range(start, end):
    
        # Start URL
        url = "http://www.priv.rs/Privatization+Agency+/80/A.shtml/seo=/companyid=" + str(x)
    
        try:
            html = scraperwiki.scrape(url)
    
            # Finds the interesting bits in the page using regular expressions
            name = rH(html, '<li class="title"><h1>(.*?) <span>| Stara Pazova<\/span><\/h1><\/li>')
            status = rH(html, '<h2>General Information</h2>[^\n]\s*<h5>- (.*?)<\/h5>')
            id_nummer = rH(html, '<li class="name">Identification Number<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
            method = rH(html, '<li class="name">Method<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
            date = rH(html, '<li class="name">Date</li>[^\n]\s*<li class="value">(.*?)</li>')
            foundation_year = rH(html, '<li class="name">Foundation Year</li>[^\n]\s*<li class="value">(.*?)</li>')
            capital_on_sale = rH(html, '<li class="name">Capital being offered for sale</li>[^\n]\s*<li class="value">(.*?)</li>')
            share_of_total_capital = rH(html, '<li class="name">% of total capital</li>[^\n]\s*<li class="value">(.*?)</li>')
            nb_employees = rH(html, '<li class="name">Number of Employees</li>[^\n]\s*<li class="value">(.*?)</li>')
            nb_employees_with_degree = rH(html, '<li class="name">Number of employees with university degree</li>[^\n]\s*<li class="value">(.*?)</li>')
            address = rH(html, '<li class="name">Address</li>[^\n]\s*<li class="value">(.*?)</li>')
            town = rH(html, '<li class="name">Town</li>[^\n]\s*<li class="value">(.*?)</li>')
            director = rH(html, '<li class="name">Director</li>[^\n]\s*<li class="value">(.*?)</li>')
            contact = rH(html, '<li class="name">Contact Person</li>[^\n]\s*<li class="value">(.*?)</li>')
            surface_for_devt = rH(html, '<td>Land for development/Construction</td>[^\n]\s*<td class="center">(.*?)</td>')
            surface_agri = rH(html, '<td>Agricultural land</td>[^\n]\s*<td class="center">(.*?)</td>')
            surface_building = rH(html, '<td>Total surface of all buildings</td>[^\n]\s*<td class="center">(.*?)</td>')
            year_of_reference = rH(html, '<tr class="head">[^\n]\s*<td>&nbsp;</td><td>.*?</td><td>(.*?)</td></tr>')
            assets = rH(html, '<td>Ukupna aktiva</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
            profits = rH(html, '<td>Neto dobitak gubitak</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
            buyer = rH(html, '<td class="w110">Pravno lice</td>[^\n]\s*<td class="w250">(.*?)</td>')
            buyer_city = rH(html, '<td class="w110">Sedište</td>[^\n]\s*<td class="w250">(.*?)</td>')
            buying_price = rH(html, '<td class="w110">Prodajna cena</td>[^\n]\s*<td class="w250">(.*?)</td>')
            date_calls = rH(html, '<td class="w160">Datum javnog poziva</td>[^\n]\s*<td class="w200">(.*?)</td>')
            date_sale = rH(html, '<td class="w110">Datum potpisivanja ugovora</td>[^\n]\s*<td class="w250">(.*?)</td>')
    
            # stores the data into an object
            data = {
                'id': x,
                'name': name,
                'status': status,
                'id_nummer': id_nummer,
                'method': method,
                'date': date,
                'foundation_year': foundation_year,
                'capital_on_sale': capital_on_sale,
                'share_of_total_capital': share_of_total_capital,
                'nb_employees': nb_employees,
                'nb_employees_with_degree': nb_employees_with_degree,
                'address': address,
                'town': town,
                'director': director,
                'contact': contact,
                'surface_for_devt': surface_for_devt,
                'surface_agri': surface_agri,
                'surface_building': surface_building,
                'year_of_reference': year_of_reference,
                'assets': assets,
                'profits': profits,
                'buyer': buyer,
                'buyer_city': buyer_city,
                'buying_price': buying_price,
                'date_calls': date_calls,
                'date_sale': date_sale
            }
        
            if (name != ""):
                # saves the object
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
        except:
            passimport scraperwiki
import re
import pprint
import math
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# This function applies the regex to the page
def rH(html, expression):
    
    regex = re.compile(expression)
       
    match = regex.findall(html)
        
    name = ""
    
    if match:
        name = match[0][1]
    
    return name

# Finds the DB that we use
scraperwiki.sqlite.attach('rs_privatizations')

# Corrective scraping: Get back all the buyers!
# First, get the records that don't have a buyer
firm_ids = scraperwiki.sqlite.execute('SELECT id FROM `rs_privatizations`.swdata WHERE buyer = "" AND status = "Sold"')

for firm_id in firm_ids['data']:

    url = "http://www.priv.rs/Privatization+Agency+/80/A.shtml/seo=/companyid=" + str(firm_id[0]) + "/lang_type=eng"
    
    html = scraperwiki.scrape(url)
    
    name = rH(html, '<li class="(title)"><h1>(.*?) <span>| Stara Pazova<\/span><\/h1><\/li>')
    status = rH(html, '<h2>(General Information)</h2>[^\n]\s*<h5>- (.*?)<\/h5>')
    id_nummer = rH(html, '<li class="name">(Identification Number)<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
    method = rH(html, '<li class="name">(Method)<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
    date = rH(html, '<li class="name">(Date)</li>[^\n]\s*<li class="value">(.*?)</li>')
    foundation_year = rH(html, '<li class="name">(Foundation Year)</li>[^\n]\s*<li class="value">(.*?)</li>')
    capital_on_sale = rH(html, '<li class="name">(Capital being offered for sale)</li>[^\n]\s*<li class="value">(.*?)</li>')
    share_of_total_capital = rH(html, '<li class="name">(% of total capital)</li>[^\n]\s*<li class="value">(.*?)</li>')
    nb_employees = rH(html, '<li class="name">(Number of Employees)</li>[^\n]\s*<li class="value">(.*?)</li>')
    nb_employees_with_degree = rH(html, '<li class="name">(Number of employees with university degree)</li>[^\n]\s*<li class="value">(.*?)</li>')
    address = rH(html, '<li class="name">(Address)</li>[^\n]\s*<li class="value">(.*?)</li>')
    town = rH(html, '<li class="name">(Town)</li>[^\n]\s*<li class="value">(.*?)</li>')
    director = rH(html, '<li class="name">(Director)</li>[^\n]\s*<li class="value">(.*?)</li>')
    contact = rH(html, '<li class="name">(Contact Person)</li>[^\n]\s*<li class="value">(.*?)</li>')
    surface_for_devt = rH(html, '<td>(Land for development/Construction)</td>[^\n]\s*<td class="center">(.*?)</td>')
    surface_agri = rH(html, '<td>(Agricultural land)</td>[^\n]\s*<td class="center">(.*?)</td>')
    surface_building = rH(html, '<td>(Total surface of all buildings)</td>[^\n]\s*<td class="center">(.*?)</td>')
    year_of_reference = rH(html, '<tr class="(head)">[^\n]\s*<td>&nbsp;</td><td>.*?</td><td>(.*?)</td></tr>')
    assets = rH(html, '<td>(Ukupna aktiva)</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
    profits = rH(html, '<td>(Neto dobitak gubitak)</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
    date_calls = rH(html, '<td class="w160">(Datum javnog poziva)</td>[^\n]\s*<td class="w200">(.*?)</td>')

    buyer = rH(html, '<td class=\"w\d{3}\">(Fizičko|Pravno) lice<\/td>[^\n]\s*<td class="w\d{3}">(.*)<\/td>')
    buyer_city = rH(html, '<td class="w\d\d\d">(Sedište)</td>[^\n]\s*<td class="w\d\d\d">(.*)</td>')
    buying_price = rH(html, '<td class="w\d\d\d">(Prodajna cena|Krajnja ponuda)</td>[^\n]\s*<td class="w\d\d\d">(.*)</td>')
    date_sale = rH(html, '<td class="w\d{3}">(Datum potpisivanja ugovora)</td>[^\n]\s*<td class="w\d{3}">(.*)</td>')

    data = {
        'id': str(firm_id[0]),
        'name': name,
        'status': status,
        'id_nummer': id_nummer,
        'method': method,
        'date': date,
        'foundation_year': foundation_year,
        'capital_on_sale': capital_on_sale,
        'share_of_total_capital': share_of_total_capital,
        'nb_employees': nb_employees,
        'nb_employees_with_degree': nb_employees_with_degree,
        'address': address,
        'town': town,
        'director': director,
        'contact': contact,
        'surface_for_devt': surface_for_devt,
        'surface_agri': surface_agri,
        'surface_building': surface_building,
        'year_of_reference': year_of_reference,
        'assets': assets,
        'profits': profits,
        'buyer': buyer,
        'buyer_city': buyer_city,
        'buying_price': buying_price,
        'date_calls': date_calls,
        'date_sale': date_sale
    }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

# Top value for a company ID. Set at zero so that no job is done
max_id = 0

# Find how many records are in the DB already
num_rows = scraperwiki.sqlite.execute('SELECT COALESCE(MAX(id)+1, 0) FROM `rs_privatizations`.swdata')

#extracts the number of records in the DB
start = num_rows['data'][0][0]
end = start + 1000

if start < max_id:
    
    #Gets down to the actual scraping
    for x in range(start, end):
    
        # Start URL
        url = "http://www.priv.rs/Privatization+Agency+/80/A.shtml/seo=/companyid=" + str(x)
    
        try:
            html = scraperwiki.scrape(url)
    
            # Finds the interesting bits in the page using regular expressions
            name = rH(html, '<li class="title"><h1>(.*?) <span>| Stara Pazova<\/span><\/h1><\/li>')
            status = rH(html, '<h2>General Information</h2>[^\n]\s*<h5>- (.*?)<\/h5>')
            id_nummer = rH(html, '<li class="name">Identification Number<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
            method = rH(html, '<li class="name">Method<\/li>[^\n]\s*<li class="value">(.*?)<\/li>')
            date = rH(html, '<li class="name">Date</li>[^\n]\s*<li class="value">(.*?)</li>')
            foundation_year = rH(html, '<li class="name">Foundation Year</li>[^\n]\s*<li class="value">(.*?)</li>')
            capital_on_sale = rH(html, '<li class="name">Capital being offered for sale</li>[^\n]\s*<li class="value">(.*?)</li>')
            share_of_total_capital = rH(html, '<li class="name">% of total capital</li>[^\n]\s*<li class="value">(.*?)</li>')
            nb_employees = rH(html, '<li class="name">Number of Employees</li>[^\n]\s*<li class="value">(.*?)</li>')
            nb_employees_with_degree = rH(html, '<li class="name">Number of employees with university degree</li>[^\n]\s*<li class="value">(.*?)</li>')
            address = rH(html, '<li class="name">Address</li>[^\n]\s*<li class="value">(.*?)</li>')
            town = rH(html, '<li class="name">Town</li>[^\n]\s*<li class="value">(.*?)</li>')
            director = rH(html, '<li class="name">Director</li>[^\n]\s*<li class="value">(.*?)</li>')
            contact = rH(html, '<li class="name">Contact Person</li>[^\n]\s*<li class="value">(.*?)</li>')
            surface_for_devt = rH(html, '<td>Land for development/Construction</td>[^\n]\s*<td class="center">(.*?)</td>')
            surface_agri = rH(html, '<td>Agricultural land</td>[^\n]\s*<td class="center">(.*?)</td>')
            surface_building = rH(html, '<td>Total surface of all buildings</td>[^\n]\s*<td class="center">(.*?)</td>')
            year_of_reference = rH(html, '<tr class="head">[^\n]\s*<td>&nbsp;</td><td>.*?</td><td>(.*?)</td></tr>')
            assets = rH(html, '<td>Ukupna aktiva</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
            profits = rH(html, '<td>Neto dobitak gubitak</td><td align="right">.*?</td><td align="right">(.*?)</td></tr>')
            buyer = rH(html, '<td class="w110">Pravno lice</td>[^\n]\s*<td class="w250">(.*?)</td>')
            buyer_city = rH(html, '<td class="w110">Sedište</td>[^\n]\s*<td class="w250">(.*?)</td>')
            buying_price = rH(html, '<td class="w110">Prodajna cena</td>[^\n]\s*<td class="w250">(.*?)</td>')
            date_calls = rH(html, '<td class="w160">Datum javnog poziva</td>[^\n]\s*<td class="w200">(.*?)</td>')
            date_sale = rH(html, '<td class="w110">Datum potpisivanja ugovora</td>[^\n]\s*<td class="w250">(.*?)</td>')
    
            # stores the data into an object
            data = {
                'id': x,
                'name': name,
                'status': status,
                'id_nummer': id_nummer,
                'method': method,
                'date': date,
                'foundation_year': foundation_year,
                'capital_on_sale': capital_on_sale,
                'share_of_total_capital': share_of_total_capital,
                'nb_employees': nb_employees,
                'nb_employees_with_degree': nb_employees_with_degree,
                'address': address,
                'town': town,
                'director': director,
                'contact': contact,
                'surface_for_devt': surface_for_devt,
                'surface_agri': surface_agri,
                'surface_building': surface_building,
                'year_of_reference': year_of_reference,
                'assets': assets,
                'profits': profits,
                'buyer': buyer,
                'buyer_city': buyer_city,
                'buying_price': buying_price,
                'date_calls': date_calls,
                'date_sale': date_sale
            }
        
            if (name != ""):
                # saves the object
                scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    
        except:
            pass