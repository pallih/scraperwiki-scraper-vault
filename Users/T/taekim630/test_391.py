from BeautifulSoup import BeautifulSoup
import urllib
 
pageFile = urllib.urlopen("http://www.random.com")
pageHtml = pageFile.read()
pageFile.close()
 
soup = BeautifulSoup("".join(pageHtml))


hello = soup.findAll("li", {"class":"menuItem"})
 
# <li class="menuItem">Home</li>, <li class="menuItem">Store</li>, <li class="menuItem">About</li>, <li class="menuItem">Videos</li>, <li class="menuItem">Music</li>, <li class="menuItem">Contact</li>




print hellofrom BeautifulSoup import BeautifulSoup
import urllib
 
pageFile = urllib.urlopen("http://www.random.com")
pageHtml = pageFile.read()
pageFile.close()
 
soup = BeautifulSoup("".join(pageHtml))


hello = soup.findAll("li", {"class":"menuItem"})
 
# <li class="menuItem">Home</li>, <li class="menuItem">Store</li>, <li class="menuItem">About</li>, <li class="menuItem">Videos</li>, <li class="menuItem">Music</li>, <li class="menuItem">Contact</li>




print hello