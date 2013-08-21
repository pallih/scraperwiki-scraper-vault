import scraperwiki
import urllib2
import lxml.etree

# url = "http://fracfocus.ca/find_well/download/BC/10203523" # original URL, works with this one

url = "http://fracfocus.ca/find_well/download/BC/10216899" #tried various PDFs, format seems the same at least for top block


pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)

print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath to find <text tags

# this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text>tags and put them all in a list variable called 'lines'

lines = root.findall('.//text[@font="3"]//b')

print lines

for line in lines:
    print line.text

record={}
try:
    record["date"] = lines[12].text
except:
    record["date"] = ""
try:
    record["province"] = lines[13].text
except:
    record["province"] = ""
try:
    record["region"] = lines[14].text
except:
     record["region"] = ""
try:
    record["long"] = lines[20].text
except:
    record["long"] = ""
try:
    record["lat"] = lines[21].text
except:
    record["lat"] = ""
try:
    record["water"] = lines[16].text
except:
    record["water"] = ""
try:
    record["operator"] = lines[18].text
except:
    record["operator"] = ""
try:
    record["wellnumber"] = lines[17].text # new
except:
    record["wellnumber"] = ""
try:
    record["wellname"] = lines[19].text
except:
    record["wellname"] = ""
try:
    record["longlatproj"] = lines[22].text # new
except:
    record["longlatproj"] = ""
try:
    record["producttype"] = lines[23].text #new
except:
    record["producttype"] = ""
try:
    record["tvd"] = lines[15].text #new
except:
    record["tvd"] = ""

print record

scraperwiki.sqlite.save(['lat'], record)

