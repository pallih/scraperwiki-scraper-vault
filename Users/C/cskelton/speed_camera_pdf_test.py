import scraperwiki
import urllib2
import lxml.etree

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)

print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath to find <text tags

# this line uses xpath, which is supported by lxml.etree (which has created root) to grab the contents of any <text>tags and put them all in a list variable called 'lines'

lines = root.findall('.//text')

#create an empty dictionary variable called 'record'

record = {}

# blank values just to reduce risk of errors

record["location"] = ""
record["code"] = ""
record["date"] = ""

# loop through each item in the list, and assign it to a variable called 'line'

uniquekey = 0

for line in lines:
    #create a variable called ‘fontvalue’, and use the get method to give it the value of the <font> attribute of 'line'
    fontvalue = line.get("font")

    print fontvalue

    if fontvalue == "3": #create a variable called 'date', use the find method to grab the contents of any <b> tag (identified with XPath) in 'line', grab the text within that, and store it in the variable
        boldtext = line.find('.//b')
        date = boldtext.text
        continue

#if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)
    if fontvalue == "5" and len(line.text)<5:
        code = line.text
        continue

#if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        record["location"] = line.text
        record["date"] = date
        record["code"] = code

    uniquekey += 1
    record["uniquekey"] = uniquekey
    print record
    scraperwiki.sqlite.save(['uniquekey'], record)
