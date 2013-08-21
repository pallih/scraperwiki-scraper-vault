import scraperwiki
import urllib2
import lxml.etree

# url = "http://fracfocus.ca/find_well/download/BC/10203523" # original URL, works with this one

url = "http://fracfocus.ca/find_well/download/BC/10216899" #tried various PDFs, format seems the same at least for top block


pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)

print "After converting to xml it has %d bytes" % len(xmldata)

print xmldata # helpful to see what order in the XML the text tags are in; sometimes top to bottom rather than left to right, which can make scraping rows of data difficult

root = lxml.etree.fromstring(xmldata)

# this line uses xpath to find <text tags

# this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text>tags and put them all in a list variable called 'lines'


# need to figure out a way to grab first page 1, then page 2, but for now going to try to figure using top as guide

lines = root.findall('.//text[@font="3"]//b')

print lines

for line in lines:
    print line.text

record={}
try:
    record["wellnumber"] = lines[17].text # new
except:
    record["wellnumber"] = ""
try:
    record["wellname"] = lines[19].text
except:
    record["wellname"] = ""


xpathtopvalue = 738 # will need to figure out a way to cycle through all possible values one by one (ie row by row); if no value then does nothing, if it does find a match then grabs all values; even if blank, can then fill down in google refine later; need to structure properly with unique-id etc so don't get duplicates and don't overwrite

xpathtext = './/text[@top="' + str(xpathtopvalue) + '"]'

texttags = root.findall(xpathtext)

# texttags = root.findall('.//text[@top="502"]')

print texttags

uniqueid = 0

for text in texttags:
    left = text.attrib.get('left')
    #convert the attribute from a string into an integer:
    leftinteger = int(left)

    print leftinteger

    if leftinteger == 59:
        record ["TradeName"] = text.text
        print record
    
    if leftinteger == 197:
        record ["Supplier"] = text.text
        print record
    
    if leftinteger == 305:
        record ["Purpose"] = text.text
        print record
    
    if leftinteger == 469:
        record ["Ingredients"] = text.text
        print record
    
    if leftinteger == 665:
        record ["ChemAbstract"] = text.text
        print record
    
    if 810 < leftinteger < 818:
        record ["MaxIngredientAdd"] = text.text
        print record
    
    if 885 < leftinteger < 905:
        record ["MaxIngredientConc"] = text.text
        print record
    
    if 975 < leftinteger < 1092:
        record ["Comments"] = text.text
        print record
    
    print record

uniqueid = uniqueid+1
record["uniqueid"] = uniqueid
        
scraperwiki.sqlite.save(['uniqueid'], record)
    
