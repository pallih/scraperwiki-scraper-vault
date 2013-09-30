import scraperwiki
import lxml.html
nextpagehtml = scraperwiki.scrape("http://haverfordpafootball.stackvarsity.com/photos/show.asp?ctid=5&tzx=FCEB1E64C1F4AD2DEF1D5EF96AE013C069603A4B6C7E045DA46D64D9927FA72B8FB34285F0608BBD9C34FAB50997CD92&i=6")
nextroot = lxml.html.fromstring(nextpagehtml)
i=0
urls={}
lis={}
for txtitem in nextroot.cssselect(".xphoto_frame td[valign='top']"):
     
     urls[i]=lxml.html.tostring(txtitem)
     i+=1
print urls[0]
#urls[0]=urls[0].replace('<br>','|')
#urls[0]=urls[0].replace('>','|')
#start = 'asdf=5;'
 #end = '123jasd'
 #s = 'asdf=5;iwantthis123jasd'
 #print((s.split(start))[1].split(end)[0])
print((urls[0].split('>'))[1].split('<')[0])
#for s in lis:
   # print s