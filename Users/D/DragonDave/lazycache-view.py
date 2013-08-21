# Blank Python
import scraperwiki,urllib2
scraperwiki.utils.httpresponseheader("Content-Type", "image/jpeg")

lazycache=scraperwiki.swimport('lazycache')
html=lazycache.lazycache('http://placekitten.com/g/200/305')
html=lazycache.lazycache('http://placekitten.com/g/200/305')
#print html

html2=urllib2.urlopen('http://placekitten.com/g/200/305').read()

assert html==html2
import base64
scraperwiki.dumpMessage({"content":base64.encodestring(html2), "message_type":"console", "encoding":"base64"})

