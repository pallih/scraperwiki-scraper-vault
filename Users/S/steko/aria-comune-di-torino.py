import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

DAILY_RUN = True

url = "http://www.comune.torino.it/ambiente/aria/qualita_aria/dati_aria/valori_annuali_pm10.shtml"
br = mechanize.Browser()
br.open(url)

allforms = br.forms()

for form in allforms:
    br.select_form(nr=0)

    for control in br.form.controls:
        if control.name == 'anno':
            years = [str(item).replace('*','') for item in control.items]
        if control.name == 'stazione':
            locations = [str(item).replace('*','') for item in control.items]

        # loop through all the options in any select (drop-down) controls
        #if control.type == 'select':
        #    for item in control.items:
        #        print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])

def extract_data(location, year):
    '''Run the scraper for a single location and year'''
    
    br.open(url)
    # First, tell Mechanize which form to submit.
    # If your form didn't have a CSS name attribute, use 'nr' instead
    # - e.g. br.select_form(nr=0) to find the first form on the page.

    br.select_form(nr=0)
    
    br["anno"] = [str(year)]
    br["stazione"] = [location]
    
    # and submit the form
    br.submit()
    
    # We can now start processing it as normal
    soup = BeautifulSoup(br.response().read())
    tables = soup.findAll('table', 'tabelladatiaria')
    
    months = {
        'GEN': '01',
        'FEB': '02',
        'MAR': '03',
        'APR': '04',
        'MAG': '05',
        'GIU': '06',
        'LUG': '07',
        'AGO': '08',
        'SET': '09',
        'OTT': '10',
        'NOV': '11',
        'DIC': '12',
    }

    store = []

    for t in tables:
        if t.findAll('td')[0].contents[0].string == 'Mese':
            continue
        month_tag = t.findAll('td')[0].contents[0].string
        month = months[month_tag]
        for n, td in enumerate(t.findAll('td')):
            if td.contents[0].string in months.keys():
                pass
            else:
                if td.contents == td.string:
                    pm10_value = td.string
                else:
                    pm10_value = td.contents[0].string
                data={'pm10_value':pm10_value, 'year': year, 'month': month, 'day': n, 'location': location}
                store.append(data)
    scraperwiki.sqlite.save(['pm10_value', 'year', 'month', 'day', 'location'], store)

for l in locations:
    if DAILY_RUN is True:
        extract_data(location=l,year=2012)
    else:
        for y in years:
            extract_data(location=l,year=y)