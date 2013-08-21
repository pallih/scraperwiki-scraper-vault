import urllib
import re

urls = ["http://google.com","http://nytimes.com","http://cnn.com","http://facebook.com","http://youtube.com"]
i=0
regex = '<title>(.+?)</title>'
pattern = re.compile(regex)

while i< len(urls):
    htmlfile = urllib.urlopen(urls[i])
    htmltext = htmlfile.read()
    titles =  re.findall(pattern,htmltext)
    print titles
    i+=1


