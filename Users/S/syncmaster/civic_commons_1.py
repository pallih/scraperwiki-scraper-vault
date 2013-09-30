import re
import urllib2

def get_hyperlinks(url, source): 
 if url.endswith("/"):
     url = url[:-1]

 urlPat = re.compile(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')')

 result = re.findall(urlPat, source)

 urlList = []

 for item in result:
     link = item[1]     
     if link.startswith("http://") and link.startswith(url):
         if link not in urlList:
             urlList.append(link)
     elif link.startswith("/"):
         link = url + link
         if link not in urlList:
             urlList.append(link)
     else:
         link = url + "/" + link
         if link not in urlList:
             urlList.append(link)
 
 return urlList

#print "Enter the URL: "
url = "http://civiccommons.org/apps"
usock = urllib2.urlopen(url)
data = usock.read()
usock.close()
print get_hyperlinks(url, data)import re
import urllib2

def get_hyperlinks(url, source): 
 if url.endswith("/"):
     url = url[:-1]

 urlPat = re.compile(r'<a [^<>]*?href=("|\')([^<>"\']*?)("|\')')

 result = re.findall(urlPat, source)

 urlList = []

 for item in result:
     link = item[1]     
     if link.startswith("http://") and link.startswith(url):
         if link not in urlList:
             urlList.append(link)
     elif link.startswith("/"):
         link = url + link
         if link not in urlList:
             urlList.append(link)
     else:
         link = url + "/" + link
         if link not in urlList:
             urlList.append(link)
 
 return urlList

#print "Enter the URL: "
url = "http://civiccommons.org/apps"
usock = urllib2.urlopen(url)
data = usock.read()
usock.close()
print get_hyperlinks(url, data)