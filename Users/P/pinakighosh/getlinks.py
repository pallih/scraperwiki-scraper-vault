import urllib2
import BeautifulSoup

count=0
request = urllib2.Request("http://www.bbc.co.uk")
response = urllib2.urlopen(request)
soup = BeautifulSoup.BeautifulSoup(response)
for a in soup.findAll('a'):
    #print type(a)
    st= str(a)
    #print st
    count+=1
    #print st[st.find('"')+1:st[st.find('"')+1:].find('"')]st[st.find('"')+1:st[st.find('"')+1:].find('"')]
print count
