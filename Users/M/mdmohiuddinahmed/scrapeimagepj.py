import scraperwiki
import lxml.html
#Photos from haverfordpafootball.stackvarsity.com
url='http://haverfordpafootball.stackvarsity.com/photos/Default.asp?page='
record={}
for serial in range(1,2):
    try:
        html=scraperwiki.scrape(url+str(serial))
    except:
        break
    root = lxml.html.fromstring(html)
    ps = root.cssselect('.album_photo_frame img')
    lss = root.cssselect('.album_photo_frame a') 
    for p in ps:
        print p.attrib['src']
    for aa in lss:
        print aa.attrib['href'] 
        
        
        
