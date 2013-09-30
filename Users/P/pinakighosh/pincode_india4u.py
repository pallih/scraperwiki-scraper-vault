import scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import string

url1="http://www.india4u.com/pincode/stateresult.asp?"
page_url="page="   ##add page number and & 'page=2&'
alphabet_url='alphabet=' ##add alphabet 'alphabet=A'
#&state=Andhra%20Pradesh"
char=string.ascii_uppercase
alpha=[]
for i in char:
    alpha.append(i)

#complete_url=url1+page_url+str(page_no)+'&'+alphabet_url+alpha+i


url='http://www.india4u.com/pincode/pinstate.asp'
http = httplib2.Http()
status, response = http.request(url)
l=[]
state=[]
state_list=[]
br1="CITY"
br2="Page :"
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href']
        if 'stateresult.asp?state=' in l:
            #print link['href']
            state_list.append(link['href'][15:].replace(' ','%20'))
            #state.append(url+link['href'])
        else:
            continue
#for i in state_list:
    #print i
pages=0
br_get_page='Page No : '
state_list=state_list[:2]
for i in state_list:
    flag_pin=False
    flag_page=False
    count_page=0
    p=dict()
    for j in alpha:
        page_count=0
        #print type(url1)
        #print type(page_url)
        #print type(alphabet_url)
        #print type(alpha)
        #print type(i)
        complete_url=url1+page_url+'1'+'&'+alphabet_url+j+i
        html=scraperwiki.scrape(complete_url)
        root=lxml.html.fromstring(html)
        #complete_url=url1+page_url+str(page_no)+'&'+alphabet_url+alpha+i
        for el in root.cssselect("table tr"):
            for el2 in el.cssselect("tr td"):
                var=el2.text_content()
                if var.count(br_get_page)>0:
                    #print "in flag"
                    if count_page<3:
                        #pages.append(var)
                        pages=var
                        count_page+=1
                if var==br_get_page:
                    flag_page=True
        
        
                if br1==el2.text_content():
                    flag_pin=True
        p[j]=pages
        #page_count=pages.split(' ')[-2]
    for j in alpha:
        for k in range(p[j]):
            #print type(url1)
            print i
            complete_url=url1+page_url+str(k)+'&'+alphabet_url+j+i
            html=scraperwiki.scrape(complete_url)
            print html
            

        

import scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import string

url1="http://www.india4u.com/pincode/stateresult.asp?"
page_url="page="   ##add page number and & 'page=2&'
alphabet_url='alphabet=' ##add alphabet 'alphabet=A'
#&state=Andhra%20Pradesh"
char=string.ascii_uppercase
alpha=[]
for i in char:
    alpha.append(i)

#complete_url=url1+page_url+str(page_no)+'&'+alphabet_url+alpha+i


url='http://www.india4u.com/pincode/pinstate.asp'
http = httplib2.Http()
status, response = http.request(url)
l=[]
state=[]
state_list=[]
br1="CITY"
br2="Page :"
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href']
        if 'stateresult.asp?state=' in l:
            #print link['href']
            state_list.append(link['href'][15:].replace(' ','%20'))
            #state.append(url+link['href'])
        else:
            continue
#for i in state_list:
    #print i
pages=0
br_get_page='Page No : '
state_list=state_list[:2]
for i in state_list:
    flag_pin=False
    flag_page=False
    count_page=0
    p=dict()
    for j in alpha:
        page_count=0
        #print type(url1)
        #print type(page_url)
        #print type(alphabet_url)
        #print type(alpha)
        #print type(i)
        complete_url=url1+page_url+'1'+'&'+alphabet_url+j+i
        html=scraperwiki.scrape(complete_url)
        root=lxml.html.fromstring(html)
        #complete_url=url1+page_url+str(page_no)+'&'+alphabet_url+alpha+i
        for el in root.cssselect("table tr"):
            for el2 in el.cssselect("tr td"):
                var=el2.text_content()
                if var.count(br_get_page)>0:
                    #print "in flag"
                    if count_page<3:
                        #pages.append(var)
                        pages=var
                        count_page+=1
                if var==br_get_page:
                    flag_page=True
        
        
                if br1==el2.text_content():
                    flag_pin=True
        p[j]=pages
        #page_count=pages.split(' ')[-2]
    for j in alpha:
        for k in range(p[j]):
            #print type(url1)
            print i
            complete_url=url1+page_url+str(k)+'&'+alphabet_url+j+i
            html=scraperwiki.scrape(complete_url)
            print html
            

        

