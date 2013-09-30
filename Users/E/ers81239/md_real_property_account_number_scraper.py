import scraperwiki
import lxml.html
import urllib
import datetime


#This scraper collects a list of valid property tax account numbers for the state of maryalnd.  Another of my scrapers will then scrape data about each account.

#TODO:  Currently this scraper doesn't handle or even notice if there is more than 1 page of results on a single day.  I'm not sure if that ever happens.



#It appears that the earliest data starts at 1/1/2008, based on some manual research.

#county_range = range(10,19) #St Mary's County is 19
#start_date = datetime.date(2008,1,1)  #History was collected on 10/9/11... we should have to run back that far again.
#start_date = datetime.date(2011,9,1)  
#end_date = datetime.date(2011,9,1) 
#end_date = datetime.date(2012,1,1)
#end_date = datetime.date(2008,1,10)

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)


def urlfordate(date, county):
    #return "http://sdatcert3.resiusa.org/rp_rewrite/results.aspx?County={county}&SearchType=SALES&FromMonth={month}&FromDay={day}&FromYear={year}&ToMonth={month}&ToDay={day}&ToYear={year}&Residential=True&NonResidential=False&Improved=True&Vacant=True&District=&Map=&BPRUC=&ALImproved=True&Unimproved=True&MultipleAccounts=True&other=True".format(county=county,year=date.year,day=date.day,month=date.month)

    return" http://sdatcert3.resiusa.org/rp_rewrite/results.aspx?County={county}&SearchType=SALES&StreetName=&StreetNumber=&FromMonth={month}&FromDay={day}&FromYear={year}&ToMonth={month}&ToDay={day}&ToYear={year}&Residential=True&NonResidential=False&Improved=True&Vacant=True&District=&Map=&BPRUC=&ALImproved=True&Unimproved=True&MultipleAccounts=True&other=True&Subdivision=".format(county=county,year=date.year,day=twodigits(date.day),month=twodigits(date.month))


def twodigits(number):
    return str(number).rjust(2,"0")


def converttodate(string):
    #takes 2011-10-07 and returns a date object
    (year,month,day) = string.split("-")
    return datetime.date(int(year),int(month),int(day))

#get a list of counties and the highest date for each
todolist = scraperwiki.sqlite.select("county, max(date_queried) from swdata group by county")



for todo in todolist:
        
        county= todo.values()[0]
        from_date = converttodate(todo.values()[1])
                


        for date in daterange(from_date,datetime.date.today()):
            print "Checking data for {date} in county {county}".format(date=date, county=county)                
            url = urlfordate(date,county)
            #print url
    
    
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
                
    
                
            count = 0 #Not sure if this is necessary.
            for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if count <= 1:
                    print "*\tSkipping Header Row {row}".format(row=row)
                    pass
                else:
                    
                    #print row
                    if len(row) == 5:
                        scraperwiki.sqlite.save(unique_keys=["transfer_date","account_identifier"], data={"date_queried":date,"transfer_date":row[0], "account_identifier":row[1], "street_location":row[2], "sale_price":row[3], "libre_folio":row[4], "county":county}, verbose=10)
                        print "*\tGood Row: {row}".format(row=row)
                    else:
                        print "*\tBad Row: {row}".format(row=row)
            print "*\t{count} rows processed.".format(count=count)
    
                                                   
    
    
                
     
    
    
        
            
        
import scraperwiki
import lxml.html
import urllib
import datetime


#This scraper collects a list of valid property tax account numbers for the state of maryalnd.  Another of my scrapers will then scrape data about each account.

#TODO:  Currently this scraper doesn't handle or even notice if there is more than 1 page of results on a single day.  I'm not sure if that ever happens.



#It appears that the earliest data starts at 1/1/2008, based on some manual research.

#county_range = range(10,19) #St Mary's County is 19
#start_date = datetime.date(2008,1,1)  #History was collected on 10/9/11... we should have to run back that far again.
#start_date = datetime.date(2011,9,1)  
#end_date = datetime.date(2011,9,1) 
#end_date = datetime.date(2012,1,1)
#end_date = datetime.date(2008,1,10)

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + datetime.timedelta(n)


def urlfordate(date, county):
    #return "http://sdatcert3.resiusa.org/rp_rewrite/results.aspx?County={county}&SearchType=SALES&FromMonth={month}&FromDay={day}&FromYear={year}&ToMonth={month}&ToDay={day}&ToYear={year}&Residential=True&NonResidential=False&Improved=True&Vacant=True&District=&Map=&BPRUC=&ALImproved=True&Unimproved=True&MultipleAccounts=True&other=True".format(county=county,year=date.year,day=date.day,month=date.month)

    return" http://sdatcert3.resiusa.org/rp_rewrite/results.aspx?County={county}&SearchType=SALES&StreetName=&StreetNumber=&FromMonth={month}&FromDay={day}&FromYear={year}&ToMonth={month}&ToDay={day}&ToYear={year}&Residential=True&NonResidential=False&Improved=True&Vacant=True&District=&Map=&BPRUC=&ALImproved=True&Unimproved=True&MultipleAccounts=True&other=True&Subdivision=".format(county=county,year=date.year,day=twodigits(date.day),month=twodigits(date.month))


def twodigits(number):
    return str(number).rjust(2,"0")


def converttodate(string):
    #takes 2011-10-07 and returns a date object
    (year,month,day) = string.split("-")
    return datetime.date(int(year),int(month),int(day))

#get a list of counties and the highest date for each
todolist = scraperwiki.sqlite.select("county, max(date_queried) from swdata group by county")



for todo in todolist:
        
        county= todo.values()[0]
        from_date = converttodate(todo.values()[1])
                


        for date in daterange(from_date,datetime.date.today()):
            print "Checking data for {date} in county {county}".format(date=date, county=county)                
            url = urlfordate(date,county)
            #print url
    
    
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
                
    
                
            count = 0 #Not sure if this is necessary.
            for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if count <= 1:
                    print "*\tSkipping Header Row {row}".format(row=row)
                    pass
                else:
                    
                    #print row
                    if len(row) == 5:
                        scraperwiki.sqlite.save(unique_keys=["transfer_date","account_identifier"], data={"date_queried":date,"transfer_date":row[0], "account_identifier":row[1], "street_location":row[2], "sale_price":row[3], "libre_folio":row[4], "county":county}, verbose=10)
                        print "*\tGood Row: {row}".format(row=row)
                    else:
                        print "*\tBad Row: {row}".format(row=row)
            print "*\t{count} rows processed.".format(count=count)
    
                                                   
    
    
                
     
    
    
        
            
        
