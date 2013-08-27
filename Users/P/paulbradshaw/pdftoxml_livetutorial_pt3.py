import scraperwiki
import urllib2
import lxml.etree

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath, which is supported by lxml.etree (which has created root)
# to grab the contents of any <text> tags
# and put them all in a list variable called 'lines'
lines = root.findall('.//text')
#create new variable which we'll use as a uniquekey, set at 0 for now.
uniquekey = 0
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create an empty dictionary variable called 'record'
    record = {}
    #create a variable called fontvalue, and 
    #use the get method to give it the value of the <font> attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '3'
    if fontvalue == "3":
        #create a variable called 'date', 
        #use the find method to grab the contents of any <b> tag (identified with XPath) in 'line'
        #grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)    
    if fontvalue == "5" and len(line.text)<5:
        #grab the text in 'line' and put it in a new variable called 'code'
        code = line.text
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #store the value of the 'code' variable in a field called 'code' in the dictionary variable 'record'
        record["code"] = code
        #add 1 to that uniquekey variable
        uniquekey += 1
        #store the value of 'uniquekey' in a field of the same name in 'record' 
        record["uniquekey"] = uniquekey
        # print the value of 'record'
        print record
        # save those values in scraperwiki's sqlite database, with 'uniquekey' as the unique key
        scraperwiki.sqlite.save(['uniquekey'], record)
import scraperwiki
import urllib2
import lxml.etree

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath, which is supported by lxml.etree (which has created root)
# to grab the contents of any <text> tags
# and put them all in a list variable called 'lines'
lines = root.findall('.//text')
#create new variable which we'll use as a uniquekey, set at 0 for now.
uniquekey = 0
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create an empty dictionary variable called 'record'
    record = {}
    #create a variable called fontvalue, and 
    #use the get method to give it the value of the <font> attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '3'
    if fontvalue == "3":
        #create a variable called 'date', 
        #use the find method to grab the contents of any <b> tag (identified with XPath) in 'line'
        #grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)    
    if fontvalue == "5" and len(line.text)<5:
        #grab the text in 'line' and put it in a new variable called 'code'
        code = line.text
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #store the value of the 'code' variable in a field called 'code' in the dictionary variable 'record'
        record["code"] = code
        #add 1 to that uniquekey variable
        uniquekey += 1
        #store the value of 'uniquekey' in a field of the same name in 'record' 
        record["uniquekey"] = uniquekey
        # print the value of 'record'
        print record
        # save those values in scraperwiki's sqlite database, with 'uniquekey' as the unique key
        scraperwiki.sqlite.save(['uniquekey'], record)
import scraperwiki
import urllib2
import lxml.etree

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath, which is supported by lxml.etree (which has created root)
# to grab the contents of any <text> tags
# and put them all in a list variable called 'lines'
lines = root.findall('.//text')
#create new variable which we'll use as a uniquekey, set at 0 for now.
uniquekey = 0
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create an empty dictionary variable called 'record'
    record = {}
    #create a variable called fontvalue, and 
    #use the get method to give it the value of the <font> attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '3'
    if fontvalue == "3":
        #create a variable called 'date', 
        #use the find method to grab the contents of any <b> tag (identified with XPath) in 'line'
        #grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)    
    if fontvalue == "5" and len(line.text)<5:
        #grab the text in 'line' and put it in a new variable called 'code'
        code = line.text
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #store the value of the 'code' variable in a field called 'code' in the dictionary variable 'record'
        record["code"] = code
        #add 1 to that uniquekey variable
        uniquekey += 1
        #store the value of 'uniquekey' in a field of the same name in 'record' 
        record["uniquekey"] = uniquekey
        # print the value of 'record'
        print record
        # save those values in scraperwiki's sqlite database, with 'uniquekey' as the unique key
        scraperwiki.sqlite.save(['uniquekey'], record)
import scraperwiki
import urllib2
import lxml.etree

url = "http://www.staffssaferroads.co.uk/media/114997/03092012_forwebsite.pdf"

pdfdata = urllib2.urlopen(url).read()

print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)

root = lxml.etree.fromstring(xmldata)

# this line uses xpath, which is supported by lxml.etree (which has created root)
# to grab the contents of any <text> tags
# and put them all in a list variable called 'lines'
lines = root.findall('.//text')
#create new variable which we'll use as a uniquekey, set at 0 for now.
uniquekey = 0
# loop through each item in the list, and assign it to a variable called 'line'
for line in lines:
    #create an empty dictionary variable called 'record'
    record = {}
    #create a variable called fontvalue, and 
    #use the get method to give it the value of the <font> attribute of 'line'
    fontvalue = line.get("font")
    #print that variable
    print fontvalue
    #if that variable has a value of '3'
    if fontvalue == "3":
        #create a variable called 'date', 
        #use the find method to grab the contents of any <b> tag (identified with XPath) in 'line'
        #grab the text within that, and store it in the variable
        date = line.find('.//b').text
        #continue on to next if statement
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is less than 5 characters (counted with the len function)    
    if fontvalue == "5" and len(line.text)<5:
        #grab the text in 'line' and put it in a new variable called 'code'
        code = line.text
        continue
    #if 'fontvalue' is 5 AND the length of the text in 'line' is more than 4 characters
    if fontvalue == "5" and len(line.text)>4:
        #grab the text in 'line' and store it in a field called 'location' in the dictionary variable 'record'
        record["location"] = line.text
        #store the value of the 'date' variable in a field called 'date' in the dictionary variable 'record'
        record["date"] = date
        #store the value of the 'code' variable in a field called 'code' in the dictionary variable 'record'
        record["code"] = code
        #add 1 to that uniquekey variable
        uniquekey += 1
        #store the value of 'uniquekey' in a field of the same name in 'record' 
        record["uniquekey"] = uniquekey
        # print the value of 'record'
        print record
        # save those values in scraperwiki's sqlite database, with 'uniquekey' as the unique key
        scraperwiki.sqlite.save(['uniquekey'], record)
