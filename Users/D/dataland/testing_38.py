import scraperwiki
import lxml.html
import urllib
import datetime


def urlforstreetname(street_name):
    return "http://arlingtonva.us/Departments/RealEstate/reassessments/scripts/SearchResults.asp?ParcelID=&StrtNum=&StrtName={street_name}&StrtType=&StrtDir=&UnitNum=&Tradename=&EconUnit=".format(street_name=street_name)

for v in ['RADFORD','RANDOLPH','RHODES','RICHMOND','RIDGEVIEW','RIVER','RIXEY','ROBERT+WALKER','ROBERTS','ROCHESTER','ROCK+SPRING','ROCKINGHAM','ROLFE','ROOSEVELT',
'ROUND+HILL','SCOTT','SHIRLEY','SHIRLINGTON','SMYTHE','SOMERSET','SOUTHGATE','SPOUT+RUN','STAFFORD','STUART','SYCAMORE','TACOMA','TAFT','TAYLOR','TAZEWELL','THOMAS',
'TORONTO','TRENTON','TRINIDAD','TROY','TUCKAHOE','UHLE','UNDERWOOD','UPLAND','UPSHUR','UPTON','UTAH','VACATION','VALLEY','VAN+BUREN','VANCE','VANDERPOOL','VEITCH',
'VENABLE','VENICE','VERMONT','VERNON','WAKEFIELD','WALTER+REED','WASHINGTON','WAYNE','WESTMORELAND','WILLIAMSBURG','WILSON','WINCHESTER','WISE','WOODLEY','WOODROW',
'WOODSTOCK','WYOMING','YORKTOWN','YUCATAN']:

    street_name = v
    print "Checking data for street name = {street_name}".format(street_name=street_name)
    url = urlforstreetname(street_name)
    #print url
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if len(row) == 3:
                    now = datetime.datetime.now()
                    data={"date_queried":str(now), "street_name":street_name, "parcel_id":row[0], "trade_name":row[1], "address":row[2]}
                    scraperwiki.sqlite.save(unique_keys=["parcel_id","address"], data=data, verbose=10)
                    #print "*\tGood Row: {row}".format(row=row)
                else:
                   print "*\tBad Row: {row}".format(row=row)
                print "*\t{count} rows processed.".format(count=count)


import scraperwiki
import lxml.html
import urllib
import datetime


def urlforstreetname(street_name):
    return "http://arlingtonva.us/Departments/RealEstate/reassessments/scripts/SearchResults.asp?ParcelID=&StrtNum=&StrtName={street_name}&StrtType=&StrtDir=&UnitNum=&Tradename=&EconUnit=".format(street_name=street_name)

for v in ['RADFORD','RANDOLPH','RHODES','RICHMOND','RIDGEVIEW','RIVER','RIXEY','ROBERT+WALKER','ROBERTS','ROCHESTER','ROCK+SPRING','ROCKINGHAM','ROLFE','ROOSEVELT',
'ROUND+HILL','SCOTT','SHIRLEY','SHIRLINGTON','SMYTHE','SOMERSET','SOUTHGATE','SPOUT+RUN','STAFFORD','STUART','SYCAMORE','TACOMA','TAFT','TAYLOR','TAZEWELL','THOMAS',
'TORONTO','TRENTON','TRINIDAD','TROY','TUCKAHOE','UHLE','UNDERWOOD','UPLAND','UPSHUR','UPTON','UTAH','VACATION','VALLEY','VAN+BUREN','VANCE','VANDERPOOL','VEITCH',
'VENABLE','VENICE','VERMONT','VERNON','WAKEFIELD','WALTER+REED','WASHINGTON','WAYNE','WESTMORELAND','WILLIAMSBURG','WILSON','WINCHESTER','WISE','WOODLEY','WOODROW',
'WOODSTOCK','WYOMING','YORKTOWN','YUCATAN']:

    street_name = v
    print "Checking data for street name = {street_name}".format(street_name=street_name)
    url = urlforstreetname(street_name)
    #print url
    html = scraperwiki.scrape(url)
    #print html
    root = lxml.html.fromstring(html)
    for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if len(row) == 3:
                    now = datetime.datetime.now()
                    data={"date_queried":str(now), "street_name":street_name, "parcel_id":row[0], "trade_name":row[1], "address":row[2]}
                    scraperwiki.sqlite.save(unique_keys=["parcel_id","address"], data=data, verbose=10)
                    #print "*\tGood Row: {row}".format(row=row)
                else:
                   print "*\tBad Row: {row}".format(row=row)
                print "*\t{count} rows processed.".format(count=count)


