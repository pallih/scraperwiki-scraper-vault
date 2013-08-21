import scraperwiki           
import lxml.html 
import uuid
import datetime

def dothework():
    #latest = scraperwiki.sqlite.execute("delete from swdata where date='02 Apr 2013'")
    #scraperwiki.sqlite.commit()
    #return

    ### share price info
    # scrape share price page
    url = "http://www.asx.com.au/asx/research/companyInfo.do?by=asxCode&asxCode=WOW"
    html = scraperwiki.scrape(url)
    wowpage = lxml.html.fromstring(html)

    # get share price table
    table = wowpage.cssselect("table#closing-prices")[0]

    # find the columns I want
    headers = table.cssselect("tr th")
    titles = {}
    for i, c in enumerate(headers):
        titles[c.text_content()] = i

    if not (titles.has_key('High') and titles.has_key('Low') and titles.has_key('Date')):
        print "Can't find titles for share price"
        return

    # extract the data
    wowdata = {}
    for row in table.cssselect("tr"):
        elements = row.cssselect("td")
        if len(elements) < max(titles['High'], titles['Low'], titles['Date']):
            continue
        date = elements[titles['Date']].text_content()
        low = elements[titles['Low']].text_content()
        high = elements[titles['High']].text_content()
        date = datetime.datetime.strptime(date, "%d %b %Y")
        wowdata[date] = [low, high]

    ###


    ### exchange rate info
    # get AUD to GBP page
    url = "http://www.exchangerates.org.uk/AUD-GBP-exchange-rate-history.html"
    html = scraperwiki.scrape(url)
    audpage = lxml.html.fromstring(html)

    # get exchange rate table
    table = audpage.cssselect("table#hist")[0]

    # find the columns I want
    headers = table.cssselect("tr th")
    titles = {}
    for i, c in enumerate(headers):
        titles[c.text_content()] = i
    
    if not (titles.has_key('Australian Dollar to British Pound') and titles.has_key('Date')):
        print "Can't find titles for exchange rate"
        return
    
    # extract the data
    auddata = {}
    for row in (table.cssselect("tr.colone") + table.cssselect("tr.coltwo")):
        elements = row.cssselect("td")
        if len(elements) < max(titles['Australian Dollar to British Pound'], titles['Date']):
            continue
        date = elements[titles['Date']].text_content()
        rate = elements[titles['Australian Dollar to British Pound']].text_content()
        date = datetime.datetime.strptime(date, "%A %d %B %Y")
        rate = rate.split("=")[1].split("GBP")[0].strip()
        auddata[date] = rate
    
    ###



    ### which dates do we want
    # get date of most recent data scraped
    dates = scraperwiki.sqlite.execute("select date from swdata")['data']
    latest = datetime.datetime.strptime(dates[0][0], "%d %b %Y")
    for day in dates:
        day = datetime.datetime.strptime(day[0], "%d %b %Y")   
        if day > latest:
            latest = day  
    print "latest: "
    print latest
    ###



    ### put it all together
    # for each day from 'latest' to today
    day = latest + datetime.timedelta(days=1)
    while day <= datetime.datetime.today():
        print day
        # check whether we have information about the day
        if wowdata.has_key(day) and auddata.has_key(day):
    
            # get prices and rate for the day
            [low, high] = wowdata[day]
            rate = auddata[day]
    
            print low, high, rate
    
            # store data
            date = datetime.datetime.strftime(day, "%d %b %Y")
            now = datetime.datetime.now()
            data = {
                'date': date,
                'low': low,
                'high': high ,
                'title': "WOW.AX share price " + str(now),
                'link': "http://www.fake.com/"+"&uuid="+str(uuid.uuid4()),
                'pubDate': str(now) ,
                'description': date + ", " + str(high) + ", " + str(low) + ", " + date + ", " + rate
            }
            scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    
        # next day
        day += datetime.timedelta(days=1)



dothework()

