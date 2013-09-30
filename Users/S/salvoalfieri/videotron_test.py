# Blank Python
import urllib
import re

htmlfile=urllib.urlopen("http://www.videotron.com/residential/television/tv-packages/basic-service/hd-basic-service") #open the url
htmltext=htmlfile.read() #convert html to text
regex='<div class="content-title">addik(.+?) <span class="channel-meta">'
pattern=re.compile(regex)
channel=re.findall(pattern,htmltext) #find all patterns in our htmltext

print channel

# Blank Python
import urllib
import re

htmlfile=urllib.urlopen("http://www.videotron.com/residential/television/tv-packages/basic-service/hd-basic-service") #open the url
htmltext=htmlfile.read() #convert html to text
regex='<div class="content-title">addik(.+?) <span class="channel-meta">'
pattern=re.compile(regex)
channel=re.findall(pattern,htmltext) #find all patterns in our htmltext

print channel

