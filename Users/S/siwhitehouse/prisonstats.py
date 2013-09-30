#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
import string
import time
import datetime
from scraperwiki import scrape

#Scrape the three web pages that list the Population in custody statistics
html0 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody.htm')
html1 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-2008.htm')
html2 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-2007.htm')

#Extract all of the xls files from the two pages that link to the monthly population figures.
prisonStats = re.findall('/(.*?)xls', html0)
prisonStats = prisonStats + re.findall('/(.*?)xls', html1)
prisonStats = prisonStats + re.findall('/(.*?)xls', html2)
#rds.homeoffice.gov.uk/rds/pdfs06/prisjul06.xls

#Somehow I've managed to pull out a substring - probably a misuse of regex in the previous block
#So, loop through prisonStats and add the correct suffix and prefix to each element
i = 0                           
for j in prisonStats:
    prisonStats[i] = 'http://www.justice.gov.uk/' + j + 'xls'
    i=i+1                          

#Use a to keep a record of where in the monthly_population list we are
a = 0
#monthly_population is a list that has as many elements as there are monthly prison stats
monthly_population = [0] * len(prisonStats)
#Loop through the monthly prison stats spreadsheets, scrape the sheets and perform some stuff on them
for k in prisonStats:
#    print k.type()
    excel = xlrd.open_workbook(file_contents=scrape(k))
    first_sheet = excel.sheet_by_index(0)
#Convert k to lowercase for easier regex matching, allocate to variable 'month'
#    print k
    month = k.lower()
    print month
#In August 2010 the population in custody tables didn't have any bloody date associated with them at all

    if month == 'http://www.justice.gov.uk/publications/docs/pop-in-custody-tables.xls':
        month = 'http://www.justice.gov.uk/publications/docs/pop-in-custody-tables-aug-2010.xls'
    print month

#Set m to 0. Then a long if...elif...elif... construct to identify a month from the filename
#There has to be a more elegant jan|feb|mar|apr . . . . way of doing this, but I can't find one that works
 
    m = 0
    if 'jan' in month:
        print 'jan'
        m = 1
    elif 'feb' in month:
        print 'feb'
        m = 2
    elif 'mar' in month:
        print 'mar'
        m = 3
    elif 'apr' in month:
        print 'apr'
        m = 4
    elif 'may' in month:
        print 'may'
        m = 5
    elif 'jun' in month:
        print 'jun'
        m = 6
    elif 'jul' in month:
        print 'jul'
        m = 7    
    elif 'aug' in month:
        print 'aug'    
        m = 8
    elif 'sep' in month:
        print 'sep'
        m = 9    
    elif 'oct' in month:
        print 'oct'
        m = 10
    elif 'nov' in month:
        print 'nov'
        m = 11    
    elif 'dec' in month:
        print 'dec'        
        m = 12
        
#Nasty bit of checking ahead. If we haven't found a month by name then check for the string '06-2009'
#This catches Jun 2009 when the filename format was changed for that one instance. If there is still no match for
#the month then print a message to show this.

    if m == 0:
        if '06-2009' in month:
            print 'jun'
            m = 6
 

#Another if...elif...elif construct to catch the year in the filename. 
            
    if '07' in month:
        y = 2007
    if '08' in month:
        y = 2008    
    if '09' in month:
        y = 2009    
    if '10' in month:
        y = 2010    
        print 10
    if '11' in month:
        y = 2011    
    if '12' in month:
        y = 2012
    if '13' in month:
        y = 2013
    if '14' in month:
        y = 2014
    if '15' in month:
        y = 2015  

        
#Reset the value of 'month' by instantiating a date object with the month and year we have extracted. 
#The day of the month is irrelevant but 28 used to indicate it is the end of the month
        
    month = datetime.date(y, m, 28)        
        
#The spreadsheets are inconsistent about where they place their columns, although the headline totals have 
#always been in the 4th row.

#Find the columns that the male population figures are in
    b0 = 0
    placeMales = [0] * 3
    for column0 in range(0,first_sheet.ncols):
        cell0 = first_sheet.cell(3,column0)
        if re.search('Male', str(cell0)) :
            placeMales[b0] = column0
            b0 = b0 +1
#Find the columns that the female population figures are in    
    b1 = 0
    placeFemales = [0] * 3
    for column1 in range(0,first_sheet.ncols):
        cell1 = first_sheet.cell(3,column1)
        if re.search('Female', str(cell1)):
            placeFemales[b1] = column1
            b1 = b1 + 1

#Find the columns that the total population figures are in    
    b2 = 0
    placeTotals = [0] * 3
    for column2 in range(0,first_sheet.ncols):
        cell2 = first_sheet.cell(3,column2)
        if re.search('Total', str(cell2)):
            placeTotals[b2] = column2
            b2 = b2 + 1
#That's the end of grabbing the headline figures. I'm interested in the figures for indeterminate sentences
#so what follows is some dicking around as I try and work out how I am going to pull those out.

#    ind = first_sheet.cell_value(21,1)
#    if ind != '':
#        print ind 

#The second column is always used to describe what the row contains. Iterate over the rows of the 
#second column and print all of the descriptions containing "indeterminate' but not 'excluding'
#    y = 0
#    for x in first_sheet.col(1):
#        z = str(x).lower()
#        print z
#        if 'indeterminate' in z:
#            if not 'excluding' in z:
#                print y, z
#        y = y + 1

#Getting there
#This will iterate over the second column in the spreadsheet, which contains the descriptions of the figures
#in the other columns across the same row. It then checks for the rows that have the word 'indeterminate'
#but not 'excluding' in their description, thus identifying the four rows with the totals of Indeterminate
#sentences in them

    i1 = 0
    placeIndeterminate = [0] * 4
    for columni1 in range(0,first_sheet.nrows):
        celli1 = str(first_sheet.cell_value(columni1,1))
        celli1 = celli1.lower()
#        print str(first_sheet.cell_value(columni1,0)) + ' ' + celli1
        if 'indeterminate' in str(celli1):
            if not 'excluding' in str(celli1):
                placeIndeterminate[i1] = columni1
                i1 = i1 + 1
    print placeIndeterminate    

#Having done that we ought to be able to search for other strings in the column and pull out their respective values
#against the columns where we know the totals, males, females etc etc are held.

#Could do with finding a way of writing functions - (def)s - to ease this process
        
        
#summary_totals is a dictionary used to hold the headline totals according to the places in the spreadsheet
#we have found them in. Note that the numbers of individuals held are converted to integers and the 
#percentage changes are rounded to two decimal places
    
    summary_totals = {'currentTotal': int(first_sheet.cell_value(5,placeTotals[1])), 'oldTotal':int(first_sheet.cell_value(5,placeTotals[0])), 'perCentChangeTotals': round(first_sheet.cell_value(5,placeTotals[2]),2), 'currentMale': int(first_sheet.cell_value(5,placeMales[1])), 'oldMales': int(first_sheet.cell_value(5,placeMales[0])), 'perCentChangeMales': round(first_sheet.cell_value(5,placeMales[2]),2), 'currentFemales': int(first_sheet.cell_value(5,placeFemales[1])), 'oldFemales': int(first_sheet.cell_value(5,placeFemales[1])), 'perCentChangeFemales': round(first_sheet.cell_value(5,placeFemales[2]),2), 'month': month, 'currentIndeterminateTotal': int(first_sheet.cell_value(placeIndeterminate[0],placeTotals[1])),'oldIntermediateTotal':int(first_sheet.cell_value(placeIndeterminate[0],placeTotals[0])),'perCentChangeTotalIntermediates': round(first_sheet.cell_value(placeIndeterminate[0],placeTotals[2])), 'currentMaleIntermediate': int(first_sheet.cell_value(placeIndeterminate[0],placeMales[1])), 'oldMaleIntermediate':int(first_sheet.cell_value(placeIndeterminate[0],placeMales[0])), 'perCentChangeMaleIntermediates':round(first_sheet.cell_value(placeIndeterminate[0],placeMales[2]))}

#Now add summarytotals to a place in the monthly_population list. As we have created a unique entry for a date
#object we can use that to sort by if we need to.

    monthly_population [a] = summary_totals
    
#    increment a
    a = a+1

#Iterate over the entries in monthly_population and save them in the datastore
for entry in monthly_population:
        unique_key = ['month']
#        print entry['month']
        if (entry['month'] != []):
            scraperwiki.datastore.save(unique_key, entry)
    

#Import the libraries containing the functions we are going to need
import scraperwiki
import xlrd
import re
import string
import time
import datetime
from scraperwiki import scrape

#Scrape the three web pages that list the Population in custody statistics
html0 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody.htm')
html1 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-2008.htm')
html2 = scraperwiki.scrape('http://www.justice.gov.uk/publications/populationincustody-2007.htm')

#Extract all of the xls files from the two pages that link to the monthly population figures.
prisonStats = re.findall('/(.*?)xls', html0)
prisonStats = prisonStats + re.findall('/(.*?)xls', html1)
prisonStats = prisonStats + re.findall('/(.*?)xls', html2)
#rds.homeoffice.gov.uk/rds/pdfs06/prisjul06.xls

#Somehow I've managed to pull out a substring - probably a misuse of regex in the previous block
#So, loop through prisonStats and add the correct suffix and prefix to each element
i = 0                           
for j in prisonStats:
    prisonStats[i] = 'http://www.justice.gov.uk/' + j + 'xls'
    i=i+1                          

#Use a to keep a record of where in the monthly_population list we are
a = 0
#monthly_population is a list that has as many elements as there are monthly prison stats
monthly_population = [0] * len(prisonStats)
#Loop through the monthly prison stats spreadsheets, scrape the sheets and perform some stuff on them
for k in prisonStats:
#    print k.type()
    excel = xlrd.open_workbook(file_contents=scrape(k))
    first_sheet = excel.sheet_by_index(0)
#Convert k to lowercase for easier regex matching, allocate to variable 'month'
#    print k
    month = k.lower()
    print month
#In August 2010 the population in custody tables didn't have any bloody date associated with them at all

    if month == 'http://www.justice.gov.uk/publications/docs/pop-in-custody-tables.xls':
        month = 'http://www.justice.gov.uk/publications/docs/pop-in-custody-tables-aug-2010.xls'
    print month

#Set m to 0. Then a long if...elif...elif... construct to identify a month from the filename
#There has to be a more elegant jan|feb|mar|apr . . . . way of doing this, but I can't find one that works
 
    m = 0
    if 'jan' in month:
        print 'jan'
        m = 1
    elif 'feb' in month:
        print 'feb'
        m = 2
    elif 'mar' in month:
        print 'mar'
        m = 3
    elif 'apr' in month:
        print 'apr'
        m = 4
    elif 'may' in month:
        print 'may'
        m = 5
    elif 'jun' in month:
        print 'jun'
        m = 6
    elif 'jul' in month:
        print 'jul'
        m = 7    
    elif 'aug' in month:
        print 'aug'    
        m = 8
    elif 'sep' in month:
        print 'sep'
        m = 9    
    elif 'oct' in month:
        print 'oct'
        m = 10
    elif 'nov' in month:
        print 'nov'
        m = 11    
    elif 'dec' in month:
        print 'dec'        
        m = 12
        
#Nasty bit of checking ahead. If we haven't found a month by name then check for the string '06-2009'
#This catches Jun 2009 when the filename format was changed for that one instance. If there is still no match for
#the month then print a message to show this.

    if m == 0:
        if '06-2009' in month:
            print 'jun'
            m = 6
 

#Another if...elif...elif construct to catch the year in the filename. 
            
    if '07' in month:
        y = 2007
    if '08' in month:
        y = 2008    
    if '09' in month:
        y = 2009    
    if '10' in month:
        y = 2010    
        print 10
    if '11' in month:
        y = 2011    
    if '12' in month:
        y = 2012
    if '13' in month:
        y = 2013
    if '14' in month:
        y = 2014
    if '15' in month:
        y = 2015  

        
#Reset the value of 'month' by instantiating a date object with the month and year we have extracted. 
#The day of the month is irrelevant but 28 used to indicate it is the end of the month
        
    month = datetime.date(y, m, 28)        
        
#The spreadsheets are inconsistent about where they place their columns, although the headline totals have 
#always been in the 4th row.

#Find the columns that the male population figures are in
    b0 = 0
    placeMales = [0] * 3
    for column0 in range(0,first_sheet.ncols):
        cell0 = first_sheet.cell(3,column0)
        if re.search('Male', str(cell0)) :
            placeMales[b0] = column0
            b0 = b0 +1
#Find the columns that the female population figures are in    
    b1 = 0
    placeFemales = [0] * 3
    for column1 in range(0,first_sheet.ncols):
        cell1 = first_sheet.cell(3,column1)
        if re.search('Female', str(cell1)):
            placeFemales[b1] = column1
            b1 = b1 + 1

#Find the columns that the total population figures are in    
    b2 = 0
    placeTotals = [0] * 3
    for column2 in range(0,first_sheet.ncols):
        cell2 = first_sheet.cell(3,column2)
        if re.search('Total', str(cell2)):
            placeTotals[b2] = column2
            b2 = b2 + 1
#That's the end of grabbing the headline figures. I'm interested in the figures for indeterminate sentences
#so what follows is some dicking around as I try and work out how I am going to pull those out.

#    ind = first_sheet.cell_value(21,1)
#    if ind != '':
#        print ind 

#The second column is always used to describe what the row contains. Iterate over the rows of the 
#second column and print all of the descriptions containing "indeterminate' but not 'excluding'
#    y = 0
#    for x in first_sheet.col(1):
#        z = str(x).lower()
#        print z
#        if 'indeterminate' in z:
#            if not 'excluding' in z:
#                print y, z
#        y = y + 1

#Getting there
#This will iterate over the second column in the spreadsheet, which contains the descriptions of the figures
#in the other columns across the same row. It then checks for the rows that have the word 'indeterminate'
#but not 'excluding' in their description, thus identifying the four rows with the totals of Indeterminate
#sentences in them

    i1 = 0
    placeIndeterminate = [0] * 4
    for columni1 in range(0,first_sheet.nrows):
        celli1 = str(first_sheet.cell_value(columni1,1))
        celli1 = celli1.lower()
#        print str(first_sheet.cell_value(columni1,0)) + ' ' + celli1
        if 'indeterminate' in str(celli1):
            if not 'excluding' in str(celli1):
                placeIndeterminate[i1] = columni1
                i1 = i1 + 1
    print placeIndeterminate    

#Having done that we ought to be able to search for other strings in the column and pull out their respective values
#against the columns where we know the totals, males, females etc etc are held.

#Could do with finding a way of writing functions - (def)s - to ease this process
        
        
#summary_totals is a dictionary used to hold the headline totals according to the places in the spreadsheet
#we have found them in. Note that the numbers of individuals held are converted to integers and the 
#percentage changes are rounded to two decimal places
    
    summary_totals = {'currentTotal': int(first_sheet.cell_value(5,placeTotals[1])), 'oldTotal':int(first_sheet.cell_value(5,placeTotals[0])), 'perCentChangeTotals': round(first_sheet.cell_value(5,placeTotals[2]),2), 'currentMale': int(first_sheet.cell_value(5,placeMales[1])), 'oldMales': int(first_sheet.cell_value(5,placeMales[0])), 'perCentChangeMales': round(first_sheet.cell_value(5,placeMales[2]),2), 'currentFemales': int(first_sheet.cell_value(5,placeFemales[1])), 'oldFemales': int(first_sheet.cell_value(5,placeFemales[1])), 'perCentChangeFemales': round(first_sheet.cell_value(5,placeFemales[2]),2), 'month': month, 'currentIndeterminateTotal': int(first_sheet.cell_value(placeIndeterminate[0],placeTotals[1])),'oldIntermediateTotal':int(first_sheet.cell_value(placeIndeterminate[0],placeTotals[0])),'perCentChangeTotalIntermediates': round(first_sheet.cell_value(placeIndeterminate[0],placeTotals[2])), 'currentMaleIntermediate': int(first_sheet.cell_value(placeIndeterminate[0],placeMales[1])), 'oldMaleIntermediate':int(first_sheet.cell_value(placeIndeterminate[0],placeMales[0])), 'perCentChangeMaleIntermediates':round(first_sheet.cell_value(placeIndeterminate[0],placeMales[2]))}

#Now add summarytotals to a place in the monthly_population list. As we have created a unique entry for a date
#object we can use that to sort by if we need to.

    monthly_population [a] = summary_totals
    
#    increment a
    a = a+1

#Iterate over the entries in monthly_population and save them in the datastore
for entry in monthly_population:
        unique_key = ['month']
#        print entry['month']
        if (entry['month'] != []):
            scraperwiki.datastore.save(unique_key, entry)
    

