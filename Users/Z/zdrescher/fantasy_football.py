from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime
from unidecode import unidecode

url = "http://games.espn.go.com/ffl/leaders?slotCategoryId=0"
page = urlopen(url) #This line defines your webpage of interest

rawText=page.read() #This function reads through the page you've defined
rawHTML=fromstring(rawText) #This variable contains a string (letters) of the raw HTML text of your website

print tostring(rawHTML)



tables = rawHTML.cssselect('table') #Now we get into sorting through that HTML code, and isolating the table you want to work with

table=tables[0] #This saves your table, isolating it from any other tables on the webpage
print tostring(table)

#header_row = table.cssselect('tr')[2] #this selects the second row, which contains the column names
#column_names = [td.text_content().replace('.','') for td in header_row.cssselect('th,td')]
#columnnames = column_names[0:15]

column_names = ['PLAYER','A', 'CA', 'PASSYDS', 'PASSTD', 'INT','B', 'RUSH', 'RUSHYDS', 'RUSHTD','C','REC', 'RECYDS', 'RECTD','RECTAR','D','2PC','FUMBLE','RETTD','E','PTS']
print column_names[0:21] #this saves those column names as a variable we can reference later
columnnames = column_names[0:21]

for tr in table.cssselect('tr')[3:]: #This selects a specific row from the third row onwards
    cellvalues = [td.text_content() for td in tr.cssselect('td')] #this saves the contents of that row as an object in our table
    data = dict(zip(columnnames, cellvalues)) #this saves the data in our set
    for key in ['PTS']:
        try: 
            data['key']=int(data['key'])  
        except:
            pass
    for key in ['PLAYER']:
        try: 
            data['key']=str(data['key'])  
        except:
            pass
    save([], data)

data['rawHTML'] = unidecode(rawText)  
print data['rawHTML']from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save
import datetime
from unidecode import unidecode

url = "http://games.espn.go.com/ffl/leaders?slotCategoryId=16"
page = urlopen(url) #This line defines your webpage of interest

rawText=page.read() #This function reads through the page you've defined
rawHTML=fromstring(rawText) #This variable contains a string (letters) of the raw HTML text of your website

print tostring(rawHTML)



tables = rawHTML.cssselect('table') #Now we get into sorting through that HTML code, and isolating the table you want to work with

table=tables[0] #This saves your table, isolating it from any other tables on the webpage
print tostring(table)

#header_row = table.cssselect('tr')[2] #this selects the second row, which contains the column names
#column_names = [td.text_content().replace('.','') for td in header_row.cssselect('th,td')]
#columnnames = column_names[0:15]

column_names = ['PLAYER','A', 'CA', 'PASSYDS', 'PASSTD', 'INT','B', 'RUSH', 'RUSHYDS', 'RUSHTD','C','REC', 'RECYDS', 'RECTD','RECTAR','D','2PC','FUMBLE','RETTD','E','PTS']
print column_names[0:21] #this saves those column names as a variable we can reference later
columnnames = column_names[0:21]

for tr in table.cssselect('tr')[3:]: #This selects a specific row from the third row onwards
    cellvalues = [td.text_content() for td in tr.cssselect('td')] #this saves the contents of that row as an object in our table
    data = dict(zip(columnnames, cellvalues)) #this saves the data in our set
    for key in ['PTS']:
        try: 
            data['key']=int(data['key'])  
        except:
            pass
    for key in ['PLAYER']:
        try: 
            data['key']=str(data['key'])  
        except:
            pass
    save([], data)

data['rawHTML'] = unidecode(rawText)  
print data['rawHTML']