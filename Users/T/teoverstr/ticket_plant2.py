import scraperwiki
import urllib2
import pandas as pd
import datetime as dt
import tables as pt

today = dt.datetime.now()

print(today.strftime('%Y%m%d'))

if today.weekday() >= 5:
    #its the weekend, do nothing and exit
    print('its the weekend, nothing to see here folks...')
else:
    #its a weekday, lets download some data
    print('its a weekday, time to get busy...')
    file_str = today.strftime('%Y%m%d') + 'h5'
    daily_archive = pd.HDFStore(file_str)
    print(daily_archive)
    daily_archive.close()


"""
class update:
    def __init__(self, timestamp = 0, open = 0.0, high = 0.0, low = 0.0, close = 0.0, volume = 0):
        self.timestamp = timestamp
        self.open   = open
        self.high   = high
        self.low    = low
        self.close  = close
        self.volume = volume

    def parse_google_update(self, new_line):
        splits = new_line.split(',')
        self.timestamp = splits[0]
        self.open   = splits[1]
        self.high   = splits[2]
        self.low    = splits[3]
        self.close  = splits[4]
        self.volume = splits[5]

    def printout(self):
        print self.timestamp + ',' + self.open + ',' + self.high + ',' + self.low + ',' + self.close


class instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.updates = []

    def add_update(self, new_update):
        self.updates.append(new_update)

root_str = 'https://www.google.com/finance/getprices?i=60&p=1d&f=d,o,h,l,c,v&df=cpct&q='

symbols = ['NFLX']

instruments = []

for symbol in symbols:
    cur_inst = instrument(symbol)
    url_str = root_str + symbol
    response = urllib2.urlopen(url_str)
    data = response.read()
    lines = data.split('\n')
    for line in lines:
        splits = line.split(',')
        if len(splits) > 2 and 'COLUMN' not in splits[0]:
            new_update = update()
            new_update.parse_google_update(line)
            cur_inst.add_update(new_update)

    instruments.append(cur_inst)

for update in cur_inst.updates:
    update.printout()


"""


