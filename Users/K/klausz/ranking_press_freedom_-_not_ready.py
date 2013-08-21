# Idea/Solution taken from Mjumbe Poe / Boston Eating Establishment Temporary Permit Suspensions

# Actually its working. 
# Possible improvements:
# - scrape all years (different link on top)
# - check if code can be improved


###############################################################################
# Ranking on Press Freedom in different countries worldwide - Reporters Sans Frontier
#
# Website: http://en.rsf.org/spip.php?page=classement&id_rubrique=1034

# Fields:
#    Rank = ''
#    Country = ''
#    Note_Mark = ''
#    Notused_Link = ''
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
#starting_url = 'http://en.rsf.org/spip.php?' #http://en.rsf.org/spip.php?page=classement&id_rubrique=1034
starting_url = 'http://en.rsf.org/spip.php?page=classement&id_rubrique=1034'
#html = scraperwiki.scrape(starting_url, {'page=classement&id_rubrique=1034'}) # thats the selection 
html = scraperwiki.scrape(starting_url,{})# thats the selection 

soup = BeautifulSoup(html)


# use BeautifulSoup to get all <td> tags
#div = soup.find('div',{'class':'contenu'}) #selects the element of the website which includes the table

div = soup.find('table',{'class':'spip'}) #selects the element of the website which includes the table


# This Block not changed - should either be corrected or be removed
# Begin 
susp_rows = div.findAll('tr') #the 'bracket around each line'

def absolutize_url(url): #it seems these are the empty line, tbchanged later
    if url[0] == '/':
        url = 'http://www.cityofboston.gov' + url#what is going on here?
    elif url[:4] != 'http':
        url = 'http://www.cityofboston.gov/isd/health/' + url    
    return url
# End

for susp_row in susp_rows[1:]:## where did this come from? Why?

# seems to be used when empty line
    Rank = ''
    Country = ''
    Note_Mark = ''
    Notused_Link = ''

   
    cells = susp_row.findAll('td')
    
#Seems to be used when there is content in Line

    Rank = cells[0].text
    Country = cells[1].text
    Note_Mark = cells[2].text
    Notused_Link = cells[3].text

# Is this necessary ? Why. Possibly when there are empty lines. It has not been changed. 
# Begin
    susp_a = cells[2].find('a')
    if susp_a:
        susp_url = absolutize_url(susp_a['href'])
    
    reinst_a = cells[3].find('a')
    if reinst_a:
        reinst_url = absolutize_url(reinst_a['href'])
# End
    

#Seems to be used when there is content in the line
# It seems to be necessary to define every column in the table, otherwise its not working
    record = {
        'Rank' : Rank,
        'Country' : Country,
        'Note' : Note_Mark,
        'Notused' : Notused_Link
    }
    
    print record
    
    scraperwiki.sqlite.save(['Country'], record)


