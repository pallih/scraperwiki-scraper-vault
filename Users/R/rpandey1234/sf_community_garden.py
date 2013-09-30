import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=209515151445316494196.0004457a5ddad6ef321a3&z=13'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div', {'class':'content_main_sub'}) 

table = div.find('table')

dept_table = table.find('table')

dept_rows = dept_table.findAll('tr')

for dept_row in dept_rows[1:]:
    cab_name = ''
    cab_url = ''
    office_holder = ''
    
    cells = dept_row.findAll('td')
    cab_cell = cells[0]

    cab_text = cab_cell.text

    cab_strong = cab_cell.find('strong')
    cab_name = cab_strong.text
    
    cab_a = cab_cell.find('a')
    if cab_a:
        cab_url = 'http://www.cityofboston.gov' + cab_a['href']
    
    office_holder = cab_text.replace(cab_name, '', 1)
    office_holder.strip()
    
    depts_cell = cells[1]
    dept_divs = depts_cell.findAll('div')

    for dept_div in dept_divs:
        dept_name = ''
        dept_url = ''

        dept_name = dept_div.text
        dept_a = dept_div.find('a')
        if dept_a:
            dept_url = dept_a['href']
            if dept_url[0] == '/':
                dept_url = 'http://www.cityofboston.gov' + dept_url
        
        record = { 
            'cab_name' : cab_name,
            'cab_url' : cab_url,
            'office_holder' : office_holder,
            'dept_name' : dept_name,
            'dept_url' : dept_url
        }
        scraperwiki.datastore.save(['cab_name','dept_name'],record)


#for td in tds:
#    print td
#    record = { "td" : td.text }
#    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&msid=209515151445316494196.0004457a5ddad6ef321a3&z=13'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
div = soup.find('div', {'class':'content_main_sub'}) 

table = div.find('table')

dept_table = table.find('table')

dept_rows = dept_table.findAll('tr')

for dept_row in dept_rows[1:]:
    cab_name = ''
    cab_url = ''
    office_holder = ''
    
    cells = dept_row.findAll('td')
    cab_cell = cells[0]

    cab_text = cab_cell.text

    cab_strong = cab_cell.find('strong')
    cab_name = cab_strong.text
    
    cab_a = cab_cell.find('a')
    if cab_a:
        cab_url = 'http://www.cityofboston.gov' + cab_a['href']
    
    office_holder = cab_text.replace(cab_name, '', 1)
    office_holder.strip()
    
    depts_cell = cells[1]
    dept_divs = depts_cell.findAll('div')

    for dept_div in dept_divs:
        dept_name = ''
        dept_url = ''

        dept_name = dept_div.text
        dept_a = dept_div.find('a')
        if dept_a:
            dept_url = dept_a['href']
            if dept_url[0] == '/':
                dept_url = 'http://www.cityofboston.gov' + dept_url
        
        record = { 
            'cab_name' : cab_name,
            'cab_url' : cab_url,
            'office_holder' : office_holder,
            'dept_name' : dept_name,
            'dept_url' : dept_url
        }
        scraperwiki.datastore.save(['cab_name','dept_name'],record)


#for td in tds:
#    print td
#    record = { "td" : td.text }
#    # save records to the datastore
#    scraperwiki.datastore.save(["td"], record) 
    