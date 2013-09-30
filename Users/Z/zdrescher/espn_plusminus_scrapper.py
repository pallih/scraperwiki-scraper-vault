from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime
from unidecode import unidecode

page = urlopen("http://espn.go.com/nhl/statistics/player/_/stat/points/sort/plusMinus/year/2012/seasontype/2") #This line defines your webpage of interest

rawText=page.read() #This function reads through the page you've defined
rawHTML=fromstring(rawText) #This variable contains a string (letters) of the raw HTML text of your website

print tostring(rawHTML)



tables = rawHTML.cssselect('table') #Now we get into sorting through that HTML code, and isolating the table you want to work with

table=tables[0] #This saves your table, isolating it from any other tables on the webpage
print tostring(table)


header_row = table.cssselect('tr')[0] #this selects the first row, which contains the column names
columnnames = [td.text_content().replace('.','') for td in header_row.cssselect('th,td')]
#this saves those column names as a variable we can reference later

for tr in table.cssselect('tr')[1:]: #This selects a specific row from the second row onwards
    cellvalues = [td.text_content() for td in tr.cssselect('td')] #this saves the contents of that row as an object in our table
    data = dict(columnnames, cellvalues)) #this saves the data in our set
    for key in ['G','A','Pts','PIM','Yrs']:
        try: 
            data['key']=int(data['key'])  
        except:
            pass
    for key in ['Birthdate']:
            try: 
                data['key']=datetime.datetime.strptime(data['key'], '%Y-%m-%d').date()
            except:
                pass

save([], data)
data['rawHTML'] = unidecode(rawText)  
print data['rawHTML']from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime
from unidecode import unidecode

page = urlopen("http://espn.go.com/nhl/statistics/player/_/stat/points/sort/plusMinus/year/2012/seasontype/2") #This line defines your webpage of interest

rawText=page.read() #This function reads through the page you've defined
rawHTML=fromstring(rawText) #This variable contains a string (letters) of the raw HTML text of your website

print tostring(rawHTML)



tables = rawHTML.cssselect('table') #Now we get into sorting through that HTML code, and isolating the table you want to work with

table=tables[0] #This saves your table, isolating it from any other tables on the webpage
print tostring(table)


header_row = table.cssselect('tr')[0] #this selects the first row, which contains the column names
columnnames = [td.text_content().replace('.','') for td in header_row.cssselect('th,td')]
#this saves those column names as a variable we can reference later

for tr in table.cssselect('tr')[1:]: #This selects a specific row from the second row onwards
    cellvalues = [td.text_content() for td in tr.cssselect('td')] #this saves the contents of that row as an object in our table
    data = dict(columnnames, cellvalues)) #this saves the data in our set
    for key in ['G','A','Pts','PIM','Yrs']:
        try: 
            data['key']=int(data['key'])  
        except:
            pass
    for key in ['Birthdate']:
            try: 
                data['key']=datetime.datetime.strptime(data['key'], '%Y-%m-%d').date()
            except:
                pass

save([], data)
data['rawHTML'] = unidecode(rawText)  
print data['rawHTML']