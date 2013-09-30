import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.mtcbus.org/Routes.asp")
root = lxml.html.fromstring(html)
node=root.cssselect("td[align='left'] select option")

for i in node:
    newHtml=scraperwiki.scrape("http://www.mtcbus.org/Routes.asp?cboRouteCode="+i.text)
    newRoot=lxml.html.fromstring(newHtml)
    newNode1=newRoot.cssselect("tr[bgcolor='#EAEAEA'] td[align='left']")
    newNode2=newRoot.cssselect("tr[bgcolor='white'] td[align='left']")
    print i.text
    routeNo=newNode1[0].text
    serviceType=newNode1[1].text
    origin=newNode1[2].text
    destination=newNode1[3].text
    stages=[]
    temp=[]
    for index in range(len(newNode1)):
        if index>3:
            temp.append(newNode1[index])
    count=0
    arr1=0
    arr2=0
    while (count< len(newNode2) *2):
        if count%2==0:
            if arr1<len(newNode2):
                stages.append(newNode2[arr1].text)
                arr1=arr1+1
        else:
            if arr2<len(temp):
                stages.append(temp[arr2].text)
                arr2=arr2+1
        count=count+1

    data={
        'routes':routeNo,
        'service':serviceType,
        'source':origin,
        'destination':destination,
        'stages':stages
    }
    scraperwiki.sqlite.save(unique_keys=['routes'], data=data)import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://www.mtcbus.org/Routes.asp")
root = lxml.html.fromstring(html)
node=root.cssselect("td[align='left'] select option")

for i in node:
    newHtml=scraperwiki.scrape("http://www.mtcbus.org/Routes.asp?cboRouteCode="+i.text)
    newRoot=lxml.html.fromstring(newHtml)
    newNode1=newRoot.cssselect("tr[bgcolor='#EAEAEA'] td[align='left']")
    newNode2=newRoot.cssselect("tr[bgcolor='white'] td[align='left']")
    print i.text
    routeNo=newNode1[0].text
    serviceType=newNode1[1].text
    origin=newNode1[2].text
    destination=newNode1[3].text
    stages=[]
    temp=[]
    for index in range(len(newNode1)):
        if index>3:
            temp.append(newNode1[index])
    count=0
    arr1=0
    arr2=0
    while (count< len(newNode2) *2):
        if count%2==0:
            if arr1<len(newNode2):
                stages.append(newNode2[arr1].text)
                arr1=arr1+1
        else:
            if arr2<len(temp):
                stages.append(temp[arr2].text)
                arr2=arr2+1
        count=count+1

    data={
        'routes':routeNo,
        'service':serviceType,
        'source':origin,
        'destination':destination,
        'stages':stages
    }
    scraperwiki.sqlite.save(unique_keys=['routes'], data=data)