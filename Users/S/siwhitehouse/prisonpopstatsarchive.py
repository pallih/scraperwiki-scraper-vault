#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
from scraperwiki import scrape

#Scrape the two web pages that list the Population in custody statistics
html0 = scraperwiki.scrape('http://www.justice.gov.uk/populationincustody.htm')
html1 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-archive.htm')

#Extract all of the xls files from the two pages that link to the monthly population figures.
prisonStats = re.findall('/(.*?)xls', html0) + re.findall('/(.*?)xls', html1)


#Somehow I've managed to pull out a substring - probably a misuse of regex in the previous block
#So, loop through prisonStats and add the correct suffix and prefix to each element
for i, j in enumerate(prisonStats):
    prisonStats[i] = 'http://www.justice.gov.uk/' + j + 'xls'

#monthly_population is a list that has as many elements as there are monthly prison stats
monthly_population = [0] * len(prisonStats)
#Loop through the monthly prison stats spreadsheets, scrape the sheets and perform some stuff on them
#Use a to keep a record of where in the monthly_population list we are
for a, k in enumerate(prisonStats):
    excel = xlrd.open_workbook(file_contents=scrape(k))
    first_sheet = excel.sheet_by_index(0)
#Find the month and year the statistics refer to by looking at the filename    
    month = re.findall("custody-(.*?).xls",k)
    print month
#The spreadsheets are inconsistent about where they place their columns, although they have always been in the 4th row
#Find the columns that the male population figures are in
    b0 = 0
    placeMales = [0] * 3
    for column0 in range(first_sheet.ncols):
        cell0 = first_sheet.cell(3,column0)
        if 'Male' in str(cell0) :
            placeMales[b0] = column0
            b0 += 1
#Find the columns that the female population figures are in    
    b1 = 0
    placeFemales = [0] * 3
    for column1 in range(first_sheet.ncols):
        cell1 = first_sheet.cell(3,column1)
        if 'Female' in str(cell1):
            placeFemales[b1] = column1
            b1 += 1

#Find the columns that the total population figures are in    
    b2 = 0
    placeTotals = [0] * 3
    for column2 in range(first_sheet.ncols):
        cell2 = first_sheet.cell(3,column2)
        if 'Total' in str(cell2):
            placeTotals[b2] = column2
            b2 += 1
    
    summary_totals = {'currentTotal': first_sheet.cell(5,placeTotals[1]), 'oldTotal': first_sheet.cell(5,placeTotals[0]), 'perCentChangeTotals': first_sheet.cell(5,placeTotals[2]), 'currentMale': first_sheet.cell(5,placeMales[1]), 'oldMales': first_sheet.cell(5,placeMales[0]), 'perCentChangeMales': first_sheet.cell(5,placeMales[2]), 'currentFemales': first_sheet.cell(5,placeFemales[1]), 'oldFemales': first_sheet.cell(5,placeFemales[1]), 'perCentChangeFemales': first_sheet.cell(5,placeFemales[2]), 'month': month}
    monthly_population [a] = summary_totals
#    print summary_totals
#print monthly_population
    
for entry in monthly_population:
    #        scraperwiki.datastore.save(["cell_value"], {"cell_value":entry})
        unique_key = ['month']
        print entry['month']
        if entry['month'] != []:
            scraperwiki.datastore.save(unique_key, entry)
    
#    scraperwiki.datastore.save(["cell_value"], {"cell_value":entry})   
            

#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
from scraperwiki import scrape

#Scrape the two web pages that list the Population in custody statistics
html0 = scraperwiki.scrape('http://www.justice.gov.uk/populationincustody.htm')
html1 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-archive.htm')

#Extract all of the xls files from the two pages that link to the monthly population figures.
prisonStats = re.findall('/(.*?)xls', html0) + re.findall('/(.*?)xls', html1)


#Somehow I've managed to pull out a substring - probably a misuse of regex in the previous block
#So, loop through prisonStats and add the correct suffix and prefix to each element
for i, j in enumerate(prisonStats):
    prisonStats[i] = 'http://www.justice.gov.uk/' + j + 'xls'

#monthly_population is a list that has as many elements as there are monthly prison stats
monthly_population = [0] * len(prisonStats)
#Loop through the monthly prison stats spreadsheets, scrape the sheets and perform some stuff on them
#Use a to keep a record of where in the monthly_population list we are
for a, k in enumerate(prisonStats):
    excel = xlrd.open_workbook(file_contents=scrape(k))
    first_sheet = excel.sheet_by_index(0)
#Find the month and year the statistics refer to by looking at the filename    
    month = re.findall("custody-(.*?).xls",k)
    print month
#The spreadsheets are inconsistent about where they place their columns, although they have always been in the 4th row
#Find the columns that the male population figures are in
    b0 = 0
    placeMales = [0] * 3
    for column0 in range(first_sheet.ncols):
        cell0 = first_sheet.cell(3,column0)
        if 'Male' in str(cell0) :
            placeMales[b0] = column0
            b0 += 1
#Find the columns that the female population figures are in    
    b1 = 0
    placeFemales = [0] * 3
    for column1 in range(first_sheet.ncols):
        cell1 = first_sheet.cell(3,column1)
        if 'Female' in str(cell1):
            placeFemales[b1] = column1
            b1 += 1

#Find the columns that the total population figures are in    
    b2 = 0
    placeTotals = [0] * 3
    for column2 in range(first_sheet.ncols):
        cell2 = first_sheet.cell(3,column2)
        if 'Total' in str(cell2):
            placeTotals[b2] = column2
            b2 += 1
    
    summary_totals = {'currentTotal': first_sheet.cell(5,placeTotals[1]), 'oldTotal': first_sheet.cell(5,placeTotals[0]), 'perCentChangeTotals': first_sheet.cell(5,placeTotals[2]), 'currentMale': first_sheet.cell(5,placeMales[1]), 'oldMales': first_sheet.cell(5,placeMales[0]), 'perCentChangeMales': first_sheet.cell(5,placeMales[2]), 'currentFemales': first_sheet.cell(5,placeFemales[1]), 'oldFemales': first_sheet.cell(5,placeFemales[1]), 'perCentChangeFemales': first_sheet.cell(5,placeFemales[2]), 'month': month}
    monthly_population [a] = summary_totals
#    print summary_totals
#print monthly_population
    
for entry in monthly_population:
    #        scraperwiki.datastore.save(["cell_value"], {"cell_value":entry})
        unique_key = ['month']
        print entry['month']
        if entry['month'] != []:
            scraperwiki.datastore.save(unique_key, entry)
    
#    scraperwiki.datastore.save(["cell_value"], {"cell_value":entry})   
            

