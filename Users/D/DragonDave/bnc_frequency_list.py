import scraperwiki,urllib2,gzip,StringIO

# Blank Python

url="http://www.kilgarriff.co.uk/BNClists/all.al.gz"
# http://www.kilgarriff.co.uk/bnc-readme.html

print "Start. ~10s"
req = urllib2.Request(url)
opener = urllib2.build_opener()
response = opener.open(req)
print "Read."
data = response.read()
data = StringIO.StringIO(data)
gzipper = gzip.GzipFile(fileobj=data)
print "Split. ~15s" 
text = gzipper.read().split("\n")
output=[]
for row in text:
    s=row.split(" ")
    try:
        output.append({'count':int(s[0]),'word':s[1],'pos':s[2],'files':int(s[3]),'ratio':float(s[0])/100106029.0}) # magic number of whole corpus.
    except Exception, e:
        print "Hit a problem with %s:%s"%(str(s),e)
        continue
        
print "Output."
print output[0:2]
print len(output)
for i in range(0,len(output),10000):
    print "attempting %d..."%i
    scraperwiki.sqlite.save(unique_keys=[], data=output[i:i+10000])
print "Done."