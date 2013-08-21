import urllib
page=urllib.request.urlopen("http://www.beans-r-us.biz/prices.html")
text=page.read().decode("utf8")
print(text)