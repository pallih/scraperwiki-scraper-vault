import scraperwiki
import lxml.html
import mechanize
url="http://www.imd.gov.in/section/nhac/distforecast/"
states=['andra-pradesh.txt','arunachal-prades.txt']
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
#for i1 in range(len(sf)):
html=scraperwiki.scrape(url+sf[0])
#root=lxml.html.fromstring(html)
#st=root.text_content()
#print 'st'
#print st
br = mechanize.Browser()
br.set_handle_robots(False)
f = br.open(url+sf[0]).read()
darray = f.split("\n") # whole page split into lists based on new line character
print 'darray'
print darray
for i in darray:
    wordsineachline = i.split(" ");
    print 'wordsineachline'
    print wordsineachline 