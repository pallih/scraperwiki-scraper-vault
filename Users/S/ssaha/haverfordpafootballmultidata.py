import scraperwiki
import lxml.html
from urlparse import urljoin

baseurl='http://haverfordpafootball.stackvarsity.com/photos/'
startpagehtml = scraperwiki.scrape("http://haverfordpafootball.stackvarsity.com/photos/Default.asp?page=5")

root = lxml.html.fromstring(startpagehtml)
record={}
urcount=0
urls={}
for photo in root.cssselect(".album_photo_frame img"):
    thumbnailurl=photo.attrib['src']
    urls[urcount]=thumbnailurl
    urcount=urcount+1
#actualurl=thumbnailurl.replace('small','large')
tcount=0
for tlinks in root.cssselect(".album_photo_frame a"):
    rurl=tlinks.attrib['href']
    furl=urljoin(baseurl,rurl)
    nextpagehtml = scraperwiki.scrape(furl)
    nextroot = lxml.html.fromstring(nextpagehtml)
    for txtitem in nextroot.cssselect(".xphoto_frame td[valign='top']"):
        htmlfragment=lxml.html.tostring(txtitem)
        htmlfragment=htmlfragment[17:-5]
        htmlfragment=htmlfragment.replace('<br>','|')
        titlearray=htmlfragment.split('|')
        break
    titlearray[2]=titlearray[2][15:]
    record["thumbnail_url"]=urls[tcount]
    record["url"]=urls[tcount].replace('small','large')
    tcount=tcount+1
    record["album_title"]=titlearray[0]
    record["title"]=titlearray[1]
    record["date_of_photo"]=titlearray[2]
    scraperwiki.sqlite.save(["url"], record)

exit()


