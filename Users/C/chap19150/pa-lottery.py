###############################################################################
# New Jersey Lottery Numbers
#
# Fields:
#   name
#   date
#   numbers
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.state.nj.us/lottery/games/current_win_num_pfv.shtml'
html = scraperwiki.scrape(starting_url)
# print html
soup = BeautifulSoup(html)

# Skip past all the cruft at the top of the page
outer_table = soup.find('table', {'width':'100%'}) 
# print outer_table
data_tables = outer_table.findAll('tr', {'class':'style16'})
outer_counter = 0

for data_table in data_tables:
    
    print data_table
    if outer_counter == 8:
        break
    elif outer_counter == 7:
        data_name = data_table.find('td', {'class':'style14'})
        name = data_name.text
        data_sets = data_table.findAll('div')
        inner_counter = 0

        for data_set in data_sets:
            if inner_counter == 0:
                day = data_set.text    
            elif inner_counter == 1:    
                month = data_set.text
            else:
                numbers = data_set.text
            inner_counter += 1
    elif outer_counter < 7:
    
        data_sets = data_table.findAll('div')
        counter = 0
    
        for data_set in data_sets:
            # print data_set
            if counter == 0:
                name = data_set.text
            elif counter == 1:
                day = data_set.text
            elif counter == 2:
                month = data_set.text
            else:
                numbers = data_set.text
        
            counter += 1
    
    date = day + " " + month
    record = {
        'name':name,
        'draw_date':date,
        'numbers':numbers,
        'record number':outer_counter
    }

    # save records to the datastore
    scraperwiki.datastore.save(["name"], record)
    outer_counter += 1


###############################################################################
# New Jersey Lottery Numbers
#
# Fields:
#   name
#   date
#   numbers
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.state.nj.us/lottery/games/current_win_num_pfv.shtml'
html = scraperwiki.scrape(starting_url)
# print html
soup = BeautifulSoup(html)

# Skip past all the cruft at the top of the page
outer_table = soup.find('table', {'width':'100%'}) 
# print outer_table
data_tables = outer_table.findAll('tr', {'class':'style16'})
outer_counter = 0

for data_table in data_tables:
    
    print data_table
    if outer_counter == 8:
        break
    elif outer_counter == 7:
        data_name = data_table.find('td', {'class':'style14'})
        name = data_name.text
        data_sets = data_table.findAll('div')
        inner_counter = 0

        for data_set in data_sets:
            if inner_counter == 0:
                day = data_set.text    
            elif inner_counter == 1:    
                month = data_set.text
            else:
                numbers = data_set.text
            inner_counter += 1
    elif outer_counter < 7:
    
        data_sets = data_table.findAll('div')
        counter = 0
    
        for data_set in data_sets:
            # print data_set
            if counter == 0:
                name = data_set.text
            elif counter == 1:
                day = data_set.text
            elif counter == 2:
                month = data_set.text
            else:
                numbers = data_set.text
        
            counter += 1
    
    date = day + " " + month
    record = {
        'name':name,
        'draw_date':date,
        'numbers':numbers,
        'record number':outer_counter
    }

    # save records to the datastore
    scraperwiki.datastore.save(["name"], record)
    outer_counter += 1


