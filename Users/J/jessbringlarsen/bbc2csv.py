import scraperwiki
import csv
import sys

scraperwiki.sqlite.attach('bbc2')

data = scraperwiki.sqlite.execute(           
    '''select home_team || '-'|| away_team as Subject,
    date as 'Start Date',
    time as 'Start Time',
    date as 'End Date',
    time as 'End Time',
    home_team as Location 
from swdata'''
)

csvout = csv.writer(sys.stdout)
csvout.writerow(data['keys'])
csvout.append('\n')

for row in data['data']:
    row = [ r.encode('utf-8') for r in row ]
    csvout.writerow(row)
