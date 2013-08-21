# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time, datetime
import scraperwiki

start = time.time()

startdate = datetime.date(2013,2,17)
oneDay = datetime.timedelta(days=1)

currDate = startdate
today = datetime.date.today()

while currDate <= today:
    datevar = str(currDate)
    epexData= urllib2.urlopen('http://www.epexspot.com/en/market-data/intraday/intraday-table/'+datevar+'/FR/').read()
    
    
    EpexSoup = BeautifulSoup(epexData)
    
    epex = EpexSoup.findAll('tr')
    j=0
    for row in epex:
        if j > 2 and j < 27:
            i=0
            valPrxVec=[]
            valHourPrx = 0.0
            hourPrx = row.findAll('td')
            for x in hourPrx:
                if i!=5:
                    i=i+1
                else:   
                    if re.search(re.compile (r"\d+\.\d*"),str(x.contents)) == None:
                        valHourPrx=0.0
                    else:
                        valHourPrx=float(re.search(re.compile (r"\d+\.\d*"),str(x.contents)).group(0))
                    data = {'Date':str(currDate), 'Hours':j-2, 'VWAP':valHourPrx}
                    print data
                    i=i+1
            print valHourPrx
            scraperwiki.sqlite.save(unique_keys=['Date'], data=data, table_name = "epexdata")
            j = j+1
        else:
            j=j+1
    currDate = currDate+oneDay

