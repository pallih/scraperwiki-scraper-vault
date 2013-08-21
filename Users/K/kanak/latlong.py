import scraperwiki
import lxml.html
from geopy import geocoders  

def getll(loc):
    g = geocoders.Google(domain='maps.google.co.uk')
    try:
        for place, (lat, lng) in g.geocode(loc,exactly_one=False):
            #print "%s: %.5f, %.5f" % (place, lat, lng)
            ltd=lat
            lngt=lng
    except:
        ltd=0
        lngt=0
    return ltd,lngt

url="http://www.imd.gov.in/section/nhac/distforecast/"
states=['andra-pradesh.txt','arunachal-prades.txt']
#for i in states:
    #print url+i
html = scraperwiki.scrape(url)
url1=url+"state_list_new.htm"
html = scraperwiki.scrape(url1)
root = lxml.html.fromstring(html)
for statecaps in root.cssselect("form"):
    st=statecaps.text_content()
state_act=st.split()
states=st.split('\t')
states.append('andra-pradesh')
states.append('arunachal-prades')
states.append('uttaranchal')
state_act.append('Andhra-pradesh')
state_act.append('Arunachal-pradesh')
state_act.append('Uttarakhand')
#for i in state_act:
    #print i

states=[states[1]]+states[4:-5]+states[-4:]
state_act=[state_act[0]]+state_act[3:33]+state_act[34:]
#for i in state_act:
    #print i
#print states
sf=[]
for i in states:
    sf.append(i.lower()+'.txt')
sl_no=0
for i1 in range(len(sf)):
    html=scraperwiki.scrape(url+sf[i1])
    root=lxml.html.fromstring(html)
    st=root.text_content()
    l1=st.split()
    district=[]

    i=0
    district=[]

    while True:

        if l1[i]=="DISTRICT":
            district.append(l1[i+2])
            i+=2
        
        if l1[i]=="(octa)":
             i+=1
             c=0
             row=[]
             while c<5:
                 row.append(l1[i])
                 c+=1
                 i+=1

        i+=1
        if i==len(l1):
            break  
    district=district[1:]
    
    #for j in district:
    for j in range(len(district)):
        lat,lng=getll(district[j]+","+state_act[i1]+",India")
        #for k in range(len(day)):
        for k in range(5):
            scraperwiki.sqlite.save(unique_keys=["sl_no"], data={"sl_no":sl_no,"state_name":state_act[i1],"district_name":district[j],"latitude":lat,"longitude":lng})
            sl_no+=1
