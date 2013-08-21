from BeautifulSoup import BeautifulSoup
import urllib2
url="http://www.utexas.edu/world/univ/alpha/"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
universities=soup.findAll('a',{'class':'institution'})
for eachuniversity in universities:
print eachuniversity['href']+","+eachuniversity.string
