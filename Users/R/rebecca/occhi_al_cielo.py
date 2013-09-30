import scraperwiki
import mechanize 
import array
from BeautifulSoup import BeautifulSoup

url = "http://www.ced.inaf.it/anagrafica/index.html"
br = mechanize.Browser()
br.open(url)

allforms = br.forms()

for form in allforms:
    br.select_form(nr=1)

    for control in br.form.controls:
        if control.name == 'sez_n':
            sezioni = [str(item).replace('*','') for item in control.items]

        # loop through all the options in any select (drop-down) controls
        #if control.type == 'select':
        #    for item in control.items:
        #        print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])

def extract_data(sezione):
    '''Run the scraper for a single quarter'''

    br.open(url)
    # First, tell Mechanize which form to submit.
    # If your form didn't have a CSS name attribute, use 'nr' instead 
    # - e.g. br.select_form(nr=0) to find the first form on the page. 

    br.select_form(nr=1)
    
    # Set the fields: 
    
    br["sez_n"] = [sezione]
    
    # and submit the form
    br.submit()
    
    # We can now start processing it as normal
    soup = BeautifulSoup(br.response().read())
    table = soup.find('table')

    if(table == None) : 
        return
    
    rows = table.findAll('tr')
    if(rows == None) : 
        return

    for tr in rows:
        cols = tr.findAll('td')
        if(cols == None) :
            continue

        fld = list()
        for td in cols:
            fld.append(str(td.find(text=True)))

        if(len(fld) > 0) :
            scraperwiki.sqlite.save(unique_keys=['matricola', 'cognome', 'nome', 'sede'], data={'matricola': fld[0], 'cognome': fld[1], 'nome': fld[2], 'sede': sezione})
        del fld


for s in sezioni:
    extract_data(sezione=s)
    print "%s done" % (s)import scraperwiki
import mechanize 
import array
from BeautifulSoup import BeautifulSoup

url = "http://www.ced.inaf.it/anagrafica/index.html"
br = mechanize.Browser()
br.open(url)

allforms = br.forms()

for form in allforms:
    br.select_form(nr=1)

    for control in br.form.controls:
        if control.name == 'sez_n':
            sezioni = [str(item).replace('*','') for item in control.items]

        # loop through all the options in any select (drop-down) controls
        #if control.type == 'select':
        #    for item in control.items:
        #        print " - - - (value, labels) =", (str(item), [label.text  for label in item.get_labels()])

def extract_data(sezione):
    '''Run the scraper for a single quarter'''

    br.open(url)
    # First, tell Mechanize which form to submit.
    # If your form didn't have a CSS name attribute, use 'nr' instead 
    # - e.g. br.select_form(nr=0) to find the first form on the page. 

    br.select_form(nr=1)
    
    # Set the fields: 
    
    br["sez_n"] = [sezione]
    
    # and submit the form
    br.submit()
    
    # We can now start processing it as normal
    soup = BeautifulSoup(br.response().read())
    table = soup.find('table')

    if(table == None) : 
        return
    
    rows = table.findAll('tr')
    if(rows == None) : 
        return

    for tr in rows:
        cols = tr.findAll('td')
        if(cols == None) :
            continue

        fld = list()
        for td in cols:
            fld.append(str(td.find(text=True)))

        if(len(fld) > 0) :
            scraperwiki.sqlite.save(unique_keys=['matricola', 'cognome', 'nome', 'sede'], data={'matricola': fld[0], 'cognome': fld[1], 'nome': fld[2], 'sede': sezione})
        del fld


for s in sezioni:
    extract_data(sezione=s)
    print "%s done" % (s)