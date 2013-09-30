import time
#import gspread
import gdata.spreadsheet.service
g = gspread.login('mohit.khatri1987@gmail.com', 'pod@+_)(')
wID = '1'
row1 ='1'
column1 = '1'
value1 = 'value'
#worksheet = g.open('DataSheet').get_worksheet(int(wID))

# Say, you need A2
#val = worksheet.cell(2, 1).value
#print val
# And then update

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

for i in range(0,100):
 worksheet = g.open('DataSheet').get_worksheet(int(i))
 worksheet.update_cell(int(row1), int(column1), value1) 
 print i
#worksheet.update_cell(2, 1, '42') 


localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

import time
#import gspread
import gdata.spreadsheet.service
g = gspread.login('mohit.khatri1987@gmail.com', 'pod@+_)(')
wID = '1'
row1 ='1'
column1 = '1'
value1 = 'value'
#worksheet = g.open('DataSheet').get_worksheet(int(wID))

# Say, you need A2
#val = worksheet.cell(2, 1).value
#print val
# And then update

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

for i in range(0,100):
 worksheet = g.open('DataSheet').get_worksheet(int(i))
 worksheet.update_cell(int(row1), int(column1), value1) 
 print i
#worksheet.update_cell(2, 1, '42') 


localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

