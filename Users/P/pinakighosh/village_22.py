import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
url="http://censusindia.gov.in/Census_Data_2001/Village_Directory/List_of_Villages/List_of_Villages_Alphabetical.aspx?cki=&State_Code=22"
import string
#create list of upper case alphabets
l=list(string.ascii_uppercase)
#create list 1-35
l1=list(range(1,36))
l2=[]
s_no=0
#convert numbers in l2 to string
for i in l1:
        l2.append(str(i))
#append a 0 for single digit numbers
for i in range(10):
    l2[i]='0'+l2[i]
state_count=0
c=1
data=[]
#run loop for all state and union territories
#while state_count<35:
while state_count<1:
#add state code to the url
    #url1=url+l2[state_count]+"&SearchKey="
    url1=url+"&SearchKey="
    state_count+=1
    count=16
    l_c=0
    #data=[]
    row=[]
#run loop for alphabets
    while count<26:
    #while count<2:
#add search alphabet to the url
        url2=url1+l[count]
        # code added by Usha Nair
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        response = br.open(url2)
        VAR1 = response.read() #reads the source file for the web page
        br.select_form(nr=0)
        br.set_all_readonly(False)
        mnext = re.search("""<a id="lnkShowAll" href="javascript:__doPostBack\('(.*?)','(.*?)'\)" style="font-family:Verdana;font-size:Smaller;">Show All""", VAR1)
        if not mnext:
            count+=1
            continue
        br["__EVENTTARGET"] = mnext.group(1)
        br["__EVENTARGUMENT"] = mnext.group(2)
        #br.find_control("btnSearch").disabled = True
        response = br.submit()
        VAR2 = response.read() # source code after submitting show all
        print "response"
        print response
        print "VAR2"
        print VAR2
        # Usha Nair till here
        #html = scraperwiki.scrape(url2)
        #root = lxml.html.fromstring(html)
        root = lxml.html.fromstring(VAR2)
        count+=1
           
#select div where data exists
        for el in root.cssselect("div#printarea td"):
#select appropriate table row
            for el2 in el.cssselect("tr.GridAlternativeRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                     row.append(el2.text_content())
                     l_c=0
                     data.append(row)
#save to data base
                     scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], "village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                     s_no+=1
                     row=[]
#select appropriate table row
            for el2 in el.cssselect("tr.GridRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                    row.append(el2.text_content())
                    l_c=0
                    data.append(row)
#save to data base
                    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], "village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                    s_no+=1
                    row=[]
print "completed scrapping"
import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
url="http://censusindia.gov.in/Census_Data_2001/Village_Directory/List_of_Villages/List_of_Villages_Alphabetical.aspx?cki=&State_Code=22"
import string
#create list of upper case alphabets
l=list(string.ascii_uppercase)
#create list 1-35
l1=list(range(1,36))
l2=[]
s_no=0
#convert numbers in l2 to string
for i in l1:
        l2.append(str(i))
#append a 0 for single digit numbers
for i in range(10):
    l2[i]='0'+l2[i]
state_count=0
c=1
data=[]
#run loop for all state and union territories
#while state_count<35:
while state_count<1:
#add state code to the url
    #url1=url+l2[state_count]+"&SearchKey="
    url1=url+"&SearchKey="
    state_count+=1
    count=16
    l_c=0
    #data=[]
    row=[]
#run loop for alphabets
    while count<26:
    #while count<2:
#add search alphabet to the url
        url2=url1+l[count]
        # code added by Usha Nair
        br = mechanize.Browser()
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        response = br.open(url2)
        VAR1 = response.read() #reads the source file for the web page
        br.select_form(nr=0)
        br.set_all_readonly(False)
        mnext = re.search("""<a id="lnkShowAll" href="javascript:__doPostBack\('(.*?)','(.*?)'\)" style="font-family:Verdana;font-size:Smaller;">Show All""", VAR1)
        if not mnext:
            count+=1
            continue
        br["__EVENTTARGET"] = mnext.group(1)
        br["__EVENTARGUMENT"] = mnext.group(2)
        #br.find_control("btnSearch").disabled = True
        response = br.submit()
        VAR2 = response.read() # source code after submitting show all
        print "response"
        print response
        print "VAR2"
        print VAR2
        # Usha Nair till here
        #html = scraperwiki.scrape(url2)
        #root = lxml.html.fromstring(html)
        root = lxml.html.fromstring(VAR2)
        count+=1
           
#select div where data exists
        for el in root.cssselect("div#printarea td"):
#select appropriate table row
            for el2 in el.cssselect("tr.GridAlternativeRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                     row.append(el2.text_content())
                     l_c=0
                     data.append(row)
#save to data base
                     scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], "village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                     s_no+=1
                     row=[]
#select appropriate table row
            for el2 in el.cssselect("tr.GridRows td"):
                if l_c<4:
                    row.append(el2.text_content())
                    l_c+=1
                else:
                    row.append(el2.text_content())
                    l_c=0
                    data.append(row)
#save to data base
                    scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":s_no,"village_name":row[1], "village_code":row[2],"Sub_district_Name":row[3],"District_Name":row[4]})
                    s_no+=1
                    row=[]
print "completed scrapping"
