import scraperwiki

# Blank Python

import urllib2
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
import csv

#f=open('wunder-data.txt','w')

# 매달, 매날짜를 순회하며 처리한다.

for m in range(1,13) :
    for d in range(1, 32) :

# 그달에 없는 날짜인지 확인 한다.
        if(m==2 and d>28) :
            break
        elif (m in [4, 6, 9, 11] and d>30):
            break

# wunderground.com 를 가져온다.
        timestamp = '2010' +str(m)+ str(d)
        print ' 데이터를 가져올 날짜: '+ timestamp
        url= "http://www.wunderground.com/history/airport/RKSS/2010/" + str(m) + "/" + str(d) + "/DailyHistory.html"
        page=urllib2.urlopen(url)


    # 페이지에서 온도 데이터를 가져온다.
        soup = BeautifulSoup(page)

    # dayTemp= soup.body.nobr.b.string
        dayTemp = soup.fetch(attrs={"class":"nobr"})[5].span.string

    # 월 번호를 출력용 타임스탬프로 변환한다.
        if len(str(m)) < 2:
            mStamp = '0' + str(m)
        else:
            mStamp= str(m)

    # 날짜 번호를 출력용 타임스탬프로 변환한다.
        if len(str(d)) < 2:
            dStamp = '0' + str(d)
        else:
            dStamp= str(d)

    # 출력용 타임스탬프를 생성한다.
        timestamp = '2010' + mStamp + dStamp

    #파일에 날짜와 기온을 기록한다.
       # f.write(timestamp + ',' + dayTemp + '\n')

        scraperwiki.sqlite.save(timestamp, dayTemp)

#f.close()
import scraperwiki

# Blank Python

import urllib2
from BeautifulSoup import BeautifulSoup
from scraperwiki import datastore
import csv

#f=open('wunder-data.txt','w')

# 매달, 매날짜를 순회하며 처리한다.

for m in range(1,13) :
    for d in range(1, 32) :

# 그달에 없는 날짜인지 확인 한다.
        if(m==2 and d>28) :
            break
        elif (m in [4, 6, 9, 11] and d>30):
            break

# wunderground.com 를 가져온다.
        timestamp = '2010' +str(m)+ str(d)
        print ' 데이터를 가져올 날짜: '+ timestamp
        url= "http://www.wunderground.com/history/airport/RKSS/2010/" + str(m) + "/" + str(d) + "/DailyHistory.html"
        page=urllib2.urlopen(url)


    # 페이지에서 온도 데이터를 가져온다.
        soup = BeautifulSoup(page)

    # dayTemp= soup.body.nobr.b.string
        dayTemp = soup.fetch(attrs={"class":"nobr"})[5].span.string

    # 월 번호를 출력용 타임스탬프로 변환한다.
        if len(str(m)) < 2:
            mStamp = '0' + str(m)
        else:
            mStamp= str(m)

    # 날짜 번호를 출력용 타임스탬프로 변환한다.
        if len(str(d)) < 2:
            dStamp = '0' + str(d)
        else:
            dStamp= str(d)

    # 출력용 타임스탬프를 생성한다.
        timestamp = '2010' + mStamp + dStamp

    #파일에 날짜와 기온을 기록한다.
       # f.write(timestamp + ',' + dayTemp + '\n')

        scraperwiki.sqlite.save(timestamp, dayTemp)

#f.close()
