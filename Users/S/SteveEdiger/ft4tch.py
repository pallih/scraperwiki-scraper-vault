from bs4 import BeautifulSoup
import urllib2


'''
This section browses the entire site archvies processing each day at a time.  
currently, it's hard-coded to a specific single day that is somewhat typical.

TO DO
Add a range of dates and wrap it around the rest of the code.

Also, set up check for last date captured and capture from the next
day forward each time the script is run.
'''

gh_url = 'http://www.freetech4teachers.com/2010_11_29_archive.html'

#get the site, open url
req = urllib2.Request(gh_url)
handler = urllib2.urlopen(req)

'''
Check success of opening page 

Write routine to store unsuccessful attempts

#print handler.getcode()
#print handler.headers.getheader('content-type')
'''
rtrn_code = handler.getcode()
#if rtrn_code <> 200
    #store page url and rtrn_code in db for later processing

#make soup
soup = BeautifulSoup(handler)
#print soup.prettify()

#get the published date for the db
for tcon in soup.find_all(attrs={'class': 'date-header'}):
    print tcon.text

#select and proces the list of articles
for art in soup.find_all(attrs={'class':'post hentry uncustomized-post-template'}):

    #print the article title and url NOTE: debug extra line after title
    print art.find('h3').text
    print art.h3.a.get('href')

    #print content without the separator class and the image, but capture urls
    for art_text in art.find_all(attrs={'class': 'post-body entry-content'}):
        print art_text
        art_text_cnt = art_text
        art_text.div.decompose()
        print art_text_cnt


'''


'''from bs4 import BeautifulSoup
import urllib2


'''
This section browses the entire site archvies processing each day at a time.  
currently, it's hard-coded to a specific single day that is somewhat typical.

TO DO
Add a range of dates and wrap it around the rest of the code.

Also, set up check for last date captured and capture from the next
day forward each time the script is run.
'''

gh_url = 'http://www.freetech4teachers.com/2010_11_29_archive.html'

#get the site, open url
req = urllib2.Request(gh_url)
handler = urllib2.urlopen(req)

'''
Check success of opening page 

Write routine to store unsuccessful attempts

#print handler.getcode()
#print handler.headers.getheader('content-type')
'''
rtrn_code = handler.getcode()
#if rtrn_code <> 200
    #store page url and rtrn_code in db for later processing

#make soup
soup = BeautifulSoup(handler)
#print soup.prettify()

#get the published date for the db
for tcon in soup.find_all(attrs={'class': 'date-header'}):
    print tcon.text

#select and proces the list of articles
for art in soup.find_all(attrs={'class':'post hentry uncustomized-post-template'}):

    #print the article title and url NOTE: debug extra line after title
    print art.find('h3').text
    print art.h3.a.get('href')

    #print content without the separator class and the image, but capture urls
    for art_text in art.find_all(attrs={'class': 'post-body entry-content'}):
        print art_text
        art_text_cnt = art_text
        art_text.div.decompose()
        print art_text_cnt


'''


'''