import scraperwiki
import lxml.html
import bs4
import urllib2

# Blank Python

#url="http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=22&ITIState=MP&ITIDistrict=CDW"
links=['http://dget.nic.in/lisdapp/ITI/List/lsttcITIProfile.asp?ListType=20&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIVerifiedDistTradeUnits.asp?ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITINVerifiedDistTradeUnits.asp?ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIDistTradeUnits.asp?ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=21&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=22&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=23&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=24&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=25&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIGovtDistTradeUnits.asp?ListType=26&ITIState=DN&ITIDistrict=DNH', 'http://dget.nic.in/lisdapp/ITI/Reports/rpttcITIDistTradeUnits.asp?ListType=33&ITIState=DN']
sl_no=0
print len(links)
for url in links:
    try:
        l_no=url[url.find('ListType=')+9:url.find('&')]
    except:
        l_no=0
    try:
        html=urllib2.urlopen(url).read()
    except:
        continue
    start=False
    soup=bs4.BeautifulSoup(html)
    start=False
    for el in soup.find_all("table"):
        for el2 in el.find_all("tr"):
            for el3 in el2.find_all("td"):
                text= el3.get_text()
                if start:
                    sl_no+=1
                    #print (text)
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Data":text,"List":l_no})
                if text.find('1.')>0:
                    start=True