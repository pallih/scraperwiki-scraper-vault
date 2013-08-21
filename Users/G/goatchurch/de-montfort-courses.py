'''Get all courses and fee information for de Montfort University'''
import urllib
import re
import urlparse
import scraperwiki

urlcourselist = "http://www.dmu.ac.uk/courses/?index=mod&list=1"
print urlcourselist
text = urllib.urlopen(urlcourselist).read()
# <p><a href="/course/economics-and-government-2230">Economics and Government</a> BA (Hons), [Undergraduate 2011]
s = re.findall('<p><a href="(.*?)">(.*?)</a>', text)
for ss in s:
    #print ss
    urlcourse = urlparse.urljoin(urlcourselist, ss[0])
    coursetext = urllib.urlopen(urlcourse).read()
    mfee = re.search('Fee information</a></h3><p><p>&pound;([\d,]+) per year', coursetext)
    #print [coursetext]
    data = { "course":ss[1], "url":urlcourse }
    if mfee:
        fee = int(re.sub(",", "", mfee.group(1)))
        data["fee"] = fee
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)
    


