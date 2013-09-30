import scraperwiki
import lxml.html
import string
url="http://www.bankifscode.com/5/PinCode/Andaman-Nicobar/A/1"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
state_list=[]
state_list_url=[]

#scrape the name of all the states
for el in root.cssselect("table#ctl00_ContentPlaceHolder1_dlState tr"):
    for el2 in el.cssselect("td div"):
        state_list.append(((string.capwords(el2.text_content(),' ')).replace('\r\n','')).replace(' ','-')[60:-24])

#create the list of url for every state
for i in state_list:
    state_list_url.append("http://www.bankifscode.com/5/PinCode/"+i)
#for i in state_list_url:
    #print i

#
count=0
row=[]
sl_no=1
alpha=list(string.ascii_uppercase)
alphbt_count=0
#print alpha
state_list_url=state_list_url[10:18]
#for i in state_list_url:
state_count=0
#print state_list_url
while state_count<8:
    print "State"+str(state_count)
    i=state_list_url[state_count]
    state_count+=1
    url=i
    alphbt_count=0
    while alphbt_count<26:
    #while alphbt_count<1:
        url=i+'/'+alpha[alphbt_count]+'/1'
        print url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        page=1
        for el in root.cssselect("span#ctl00_ContentPlaceHolder1_lblPages p"):
            p=el.text_content().split()
            page=int(p[2])
        for j in range(page):
            z=j+1
            z=str(z)
            url=i+'/'+alpha[alphbt_count]+'/'+z
            print url
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for el in root.cssselect("table#ctl00_ContentPlaceHolder1_Result tr"):
                    for el2 in el.cssselect("td"):
                        #print el2.text_content()
                        if count is 2:
                            row.append((((string.capwords(el2.text_content(),' ')).replace('\r\n',''))[60:-24].replace('\t','')))
                            #row.append(el2.text_content())
                            #print row[2]
                        else:
                            row.append(el2.text_content())
                        count+=1
                        #print count
                    if count>2:
                        #print ("in save")
                        count=0
                        scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"state":row[0],"district":row[1],"city":row[2],"pincode":row[3]})
                        sl_no+=1
                        row=[]
        alphbt_count+=1
    

    




import scraperwiki
import lxml.html
import string
url="http://www.bankifscode.com/5/PinCode/Andaman-Nicobar/A/1"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
state_list=[]
state_list_url=[]

#scrape the name of all the states
for el in root.cssselect("table#ctl00_ContentPlaceHolder1_dlState tr"):
    for el2 in el.cssselect("td div"):
        state_list.append(((string.capwords(el2.text_content(),' ')).replace('\r\n','')).replace(' ','-')[60:-24])

#create the list of url for every state
for i in state_list:
    state_list_url.append("http://www.bankifscode.com/5/PinCode/"+i)
#for i in state_list_url:
    #print i

#
count=0
row=[]
sl_no=1
alpha=list(string.ascii_uppercase)
alphbt_count=0
#print alpha
state_list_url=state_list_url[10:18]
#for i in state_list_url:
state_count=0
#print state_list_url
while state_count<8:
    print "State"+str(state_count)
    i=state_list_url[state_count]
    state_count+=1
    url=i
    alphbt_count=0
    while alphbt_count<26:
    #while alphbt_count<1:
        url=i+'/'+alpha[alphbt_count]+'/1'
        print url
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        page=1
        for el in root.cssselect("span#ctl00_ContentPlaceHolder1_lblPages p"):
            p=el.text_content().split()
            page=int(p[2])
        for j in range(page):
            z=j+1
            z=str(z)
            url=i+'/'+alpha[alphbt_count]+'/'+z
            print url
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for el in root.cssselect("table#ctl00_ContentPlaceHolder1_Result tr"):
                    for el2 in el.cssselect("td"):
                        #print el2.text_content()
                        if count is 2:
                            row.append((((string.capwords(el2.text_content(),' ')).replace('\r\n',''))[60:-24].replace('\t','')))
                            #row.append(el2.text_content())
                            #print row[2]
                        else:
                            row.append(el2.text_content())
                        count+=1
                        #print count
                    if count>2:
                        #print ("in save")
                        count=0
                        scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"state":row[0],"district":row[1],"city":row[2],"pincode":row[3]})
                        sl_no+=1
                        row=[]
        alphbt_count+=1
    

    




