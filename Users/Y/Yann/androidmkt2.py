#import relevan libraries
import scraperwiki
import urllib, lxml.html, re
import time

#set the beginning of the urls to be scrapped
AddressInit = "https://market.android.com/details?id=apps_topselling_free&start="
id = 1
#set the number of pages to be scrapped 
NbPage = range(0, 1)

for i in NbPage: 
#build the complete URL of the page to be scrapped 
    url = str(AddressInit)+str(i*24)+'&num=24'
#get the page as htm
    f = urllib.urlopen(url)
    html = f.read()
    f.close()
#transform page in xml
    pageall= lxml.html.fromstring(html)
    titleall = pageall.cssselect('div.snippet.snippet-medium')
#iterate through each title within the page
    for i in range (0,24):
        tds = titleall[i]
        title=tds.cssselect('a.title')[0].text_content()
        urlid=tds.cssselect('a.title')[0].xpath('@href')[0]
        author=tds.cssselect('span.attribution')[0].text_content()
        rank=tds.cssselect('div.ordinal-value')[0].text_content()
#open the app specific page to gather additionnal data
        urlapp='https://market.android.com'+str(urlid)
        fapp = urllib.urlopen(urlapp)
        htmlapp = fapp.read()
        fapp.close()
        pageapp= lxml.html.fromstring(htmlapp)
        listall = pageapp.cssselect('dl.doc-metadata-list')
        listallsep=listall[0].xpath('//dd')
#fetch the number of comments and the date of last release of the app and strip commentnumb of unwanted chars
        commentnumb=listallsep[0].text_content()
        commentnumb=commentnumb.replace('(','').replace(')','').replace(',','').lstrip()
        lastrelease=listallsep[1].text_content()
#add a time stamp
        t=time.time()
#write data in table androidmkt
        data = {
               'timestamp': t,
               'title' : title,
               'author' : author,
               'rank' :  rank,
               'lastrelease' : lastrelease,
               'commentnumb' : commentnumb,
               'urlid' : urlid
            }
        scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="androidmkt") 
#import relevan libraries
import scraperwiki
import urllib, lxml.html, re
import time

#set the beginning of the urls to be scrapped
AddressInit = "https://market.android.com/details?id=apps_topselling_free&start="
id = 1
#set the number of pages to be scrapped 
NbPage = range(0, 1)

for i in NbPage: 
#build the complete URL of the page to be scrapped 
    url = str(AddressInit)+str(i*24)+'&num=24'
#get the page as htm
    f = urllib.urlopen(url)
    html = f.read()
    f.close()
#transform page in xml
    pageall= lxml.html.fromstring(html)
    titleall = pageall.cssselect('div.snippet.snippet-medium')
#iterate through each title within the page
    for i in range (0,24):
        tds = titleall[i]
        title=tds.cssselect('a.title')[0].text_content()
        urlid=tds.cssselect('a.title')[0].xpath('@href')[0]
        author=tds.cssselect('span.attribution')[0].text_content()
        rank=tds.cssselect('div.ordinal-value')[0].text_content()
#open the app specific page to gather additionnal data
        urlapp='https://market.android.com'+str(urlid)
        fapp = urllib.urlopen(urlapp)
        htmlapp = fapp.read()
        fapp.close()
        pageapp= lxml.html.fromstring(htmlapp)
        listall = pageapp.cssselect('dl.doc-metadata-list')
        listallsep=listall[0].xpath('//dd')
#fetch the number of comments and the date of last release of the app and strip commentnumb of unwanted chars
        commentnumb=listallsep[0].text_content()
        commentnumb=commentnumb.replace('(','').replace(')','').replace(',','').lstrip()
        lastrelease=listallsep[1].text_content()
#add a time stamp
        t=time.time()
#write data in table androidmkt
        data = {
               'timestamp': t,
               'title' : title,
               'author' : author,
               'rank' :  rank,
               'lastrelease' : lastrelease,
               'commentnumb' : commentnumb,
               'urlid' : urlid
            }
        scraperwiki.sqlite.save(unique_keys=["timestamp"], data=data, table_name="androidmkt") 
