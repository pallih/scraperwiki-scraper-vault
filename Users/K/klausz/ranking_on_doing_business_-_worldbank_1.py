# Idea/Solution taken from Mjumbe Poe / Boston Eating Establishment Temporary Permit Suspensions

# Open issues: The data in the sqlite table - is there a header with the column names ?
# Selction in Link was not working
# Order of columns different to what is on the website
# Using Google Chrome to get the element Information for the code, then it was relatively easy. 

###############################################################################
# Ranking of Doing Business - Worldbank - a comparison/ranking
#
# Website: http://www.doingbusiness.org/rankings
# Fields:
#    Economy = ''
#    Ease_Of_Doing_Business_Rank = ''
#    StartingABusiness = ''
#    DealingWithConstructionPermits = ''
#    RegisteringProperty = ''
#    GettingCredit = ''
#    ProtectingInvestors = ''
#    PayingTaxes = ''
#    TradingAcrossBorders = ''
#    EnforcingContracts = ''
#    ClosingABusiness =''#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.doingbusiness.org/rankings'
html = scraperwiki.scrape(starting_url, {'Rankings by region':'5'})# thats the timerange selected - 5 is OECD 
soup = BeautifulSoup(html)


# use BeautifulSoup to get all <td> tags
div = soup.find('div',{'class':'section lead clearfix'}) #selects the element of the website which includes the table
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
    Economy = ''
    Ease_Of_Doing_Business_Rank = ''
    StartingABusiness = ''
    DealingWithConstructionPermits = ''
    RegisteringProperty = ''
    GettingCredit = ''
    ProtectingInvestors = ''
    PayingTaxes = ''
    TradingAcrossBorders = ''
    EnforcingContracts = ''
    ClosingABusiness =''


    
    cells = susp_row.findAll('td')
    
#Seems to be used when there is content in Line

    Economy = cells[0].text
    Ease_Of_Doing_Business_Rank= cells[1].text
    StartingABusiness = cells[2].text
    DealingWithConstructionPermits = cells[3].text
    RegisteringProperty = cells[4].text
    GettingCredit = cells[5].text
    ProtectingInvestors = cells[6].text
    PayingTaxes = cells[7].text
    TradingAcrossBorders = cells[8].text
    EnforcingContracts = cells[9].text
    ClosingABusiness = cells[10].text


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
    record = {
        'EconomyCountry' : Economy,
        'RankDo' : Ease_Of_Doing_Business_Rank,
        'RankStart' : StartingABusiness,
        'RankConstrPerm' : DealingWithConstructionPermits,
        'RankProperty' : RegisteringProperty,
        'RankGetCredit' : GettingCredit,
        'RankInvestorProtection' : ProtectingInvestors,
        'RankPayingTaxes' : PayingTaxes,
        'RankBordertrade' : TradingAcrossBorders,
        'RankContractenforcement' : EnforcingContracts,
        'RankEndBusiness' : ClosingABusiness
        }
    
    print record
    
    scraperwiki.sqlite.save(['EconomyCountry'], record)

