import scraperwiki
#import urllib
from BeautifulSoup import BeautifulSoup

try:
    scraperwiki.sqlite.execute("drop table if exists UN_SOC_IND")
    scraperwiki.sqlite.execute("drop table if exists UN_SOC_IND_EDU")
    scraperwiki.sqlite.execute("create table UN_SOC_IND_EDU(`country` string, `year` string, `year_note` string, `total` int, `total_note` string, `men` int, `men_note` string, `women` int)")
except:
    pass


#html = urllib.urlopen("http://unstats.un.org/unsd/demographic/products/socind/education.htm").read()
#html = open('file.txt').read()
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")

pageSoup = BeautifulSoup (html)

# The table with the data
dataTable = pageSoup.findAll("table", attrs={"cellspacing" : "0", "cellpadding" : "0", "align" : "left"})[0]

# Creating a dictionary out of the reference table (end of the HTML page)
refTable = pageSoup.findAll("table", attrs={"cellspacing" : "0", "cellpadding" : "0"})[6]
refTableRowsList = refTable.findAll('tr')
refDict = {'': ''}

for refRow in refTableRowsList:
    key = str(refRow.findAll('div')[0].contents[0]).replace(' ', '') # Some of the keys have an extra space
    value = str(refRow.findAll('td')[1].contents[0])
    refDict[key] = value

# Done with the references, back to main data

# Finding all the rows in the data table
dataTableRowsList = dataTable.findAll('tr')

# Remove the header as well as redundant rows
del dataTableRowsList[0:4]

for row in dataTableRowsList:
    columns = row.findAll('td')
    
    countryName = str(columns[0].contents[0])
    year = str(columns[1].contents[0])
    
    if len(columns[3].contents) > 0:
        yearNote = columns[3].contents[0]
    else:
        yearNote = ''
    
    total = str(columns[4].contents[0])
    
    if len(columns[6].contents) > 0:
        totalNote = str(columns[6].contents[0])
    else:
        totalNote = ''
    men = str(columns[7].contents[0])
    
    if len(columns[9].contents) > 0:
        menNote = str(columns[9].contents[0])
    else:
        menNote = ''
    
    women = str(columns[10].contents[0])
    
    #print (countryName, year, refDict[yearNote], total, refDict[totalNote], men, refDict[menNote], women)
    scraperwiki.sqlite.execute("insert into UN_SOC_IND_EDU values (?,?,?,?,?,?,?,?)", (countryName, year, refDict[yearNote], total, refDict[totalNote], men, refDict[menNote], women))

scraperwiki.sqlite.commit()

