import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser
import datetime

# Royal society fellows scraper,
# Source is:
# http://royalsociety.org/uploadedFiles/Royal_Society_Content/about-us/fellowship/Fellows1660-2007.pdf
# Ignore the front page saying A-J, the whole list is in there
# p5 start of records proper
# p195-198 are a second frontpiece
# p199-formated differently?
# We're going to use pdftoxml:
# http://linux.die.net/man/1/pdftohtml
# Some examples:
# https://scraperwiki.com/views/pdf_to_html_preview_4/edit/
# https://scraperwiki.com/scrapers/new/python?template=advanced-scraping-pdfs
#

# Most lifespans are separated by - but some are separated by en dash \u2013 and some are just "flourished" denoted by fl and a single year
# Wollaston was only president for less than a year so his PRS field is different from the rest
# Successful run should produce 8019 fellows.
# Parsing lifespan dates but only if they strictly conform to %d %B %Y format
# https://scraperwiki.com/docs/python/python_time_guide/ 
# Ian Hopkinson (9/12/12)

# Borrowed from Thomas Levine's blog post on handling exceptions
def parseLifeSpan(source):
    try:
         cleandate = datetime.datetime.strptime(source.strip(), '%d %B %Y')
    except ValueError:
         cleandate = None

    return cleandate

url = "http://royalsociety.org/uploadedFiles/Royal_Society_Content/about-us/fellowship/Fellows1660-2007.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

# Page 5 is the first one to contain useful stuff
# options="-f 5 -l 20"
options="-f 5"
# options="-f 108 -l 140"

ResumeAtPage = 4
xmldata = scraperwiki.pdftoxml(pdfdata,options)

print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 11000 characters are: ", xmldata[:11000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)
UnknownID=1

for page in pages:
    pagenumber=int(page.attrib.get("number"))
    if pagenumber < ResumeAtPage:
        print "Skipping page %d, before ResumeAtPage" % pagenumber
        continue 
    if pagenumber>194 and pagenumber<199:
        print "Skipping page %d because it is frontmatter:" % pagenumber
        continue
    print "Processing page: ", pagenumber
# Don't appear to get styling info (i.e. bold)
# Fellow names have left="135" tag
# Lifespan string have left="188" tag (but alias info also appears here- ther can be more than one - see Anglesey) (one appears at 193 on p117)
# Fellow class has left="560" except after p199 when it is "540"
# Election Date has left="661" except after p199 when it is "648" 
# President has indicative text in fellow class column on same line as name (fellow is on following line)
# Wierd stuff on George II-IV "Royal Fellow; Patron 1820 18/05/1820" (appears at 496 or 518)
    if pagenumber>198:
        FellowClassCol=540
        ElectionDateCol=648
    else:
        FellowClassCol=560
        ElectionDateCol=661

    #print FellowClassCol, ElectionDateCol

    for textchunk in (page is not None and page.xpath('text')):
        leftcoord = int(textchunk.attrib.get('left'))
        if leftcoord==135: #Get a FellowName this is the restart signal
            if textchunk.text is not None and not textchunk.text.isspace():
                Fellow={}
                Fellow={'Name':textchunk.text.strip()}
        elif leftcoord>187 and leftcoord<200: #Get a lifespan string - if this is a see... then we need to write an alias
            if textchunk.text is not None and not textchunk.text.isspace():
                if textchunk.text[0:3]=="See":
                    AliasRecord={'Name':Fellow['Name'],'Alias':textchunk.text[4:].strip()}
                    scraperwiki.sqlite.save(unique_keys=["Name"],data=AliasRecord, table_name="RoyalSocietyFellowAliases")
                    # print '''It's an alias!'''
                else:
                    Fellow.update({'LifeSpan':textchunk.text.strip()})
        elif leftcoord>495 and leftcoord<570: #Get a Fellow class - need to handle presidents here Atiyah is the first
            if textchunk.text is not None and not textchunk.text.isspace():
                if textchunk.text[0:3]=="PRS":
                    #Fellow.update({'President':textchunk.text[4:].strip()})
                    part=textchunk.text[4:].split('-')
                    if len(part)==2:
                        #Fellow.update({'StartPresident':part[0].strip()})
                        #Fellow.update({'EndPresident':part[1].strip()})
                        print Fellow
                        Fellow.update({'StartPresident':datetime.datetime.strptime(part[0].strip(), '%Y').date()})
                        # At the time of publication Robert May was President, this handles the "open" end of his presidency 
                        try:
                            Fellow.update({'EndPresident':datetime.datetime.strptime(part[1].strip(), '%Y').date()})
                        except ValueError:
                            print "Handling Robert May as an exception"
                    else:
                        # Wollaston was only President for 1 year
                        # Fellow.update({'StartPresident':part[0].strip()})
                        Fellow.update({'StartPresident':datetime.datetime.strptime(part[0].strip(), '%Y').date()})
                    print "President"
                    print Fellow
                else:
                    #Fellow.update({'President':' '})
                    Fellow.update({'Class':textchunk.text.strip()})
        elif leftcoord>640: #Get a Fellow election date, get one of these and we should write the set to a structure or maybe the SQL store
            if textchunk.text is not None and not textchunk.text.isspace():
                # Handle another exception, this is the elected date for Gordon Henry Dixon, it's either 1978. 
                if textchunk.text.strip()=='16/03/197':
                     textchunk.text='16/03/1978'
                # Another exception Poulett, John, 1st Earl Poulett - seems to have two election dates separated by a ;
                try:
                    Fellow.update({'Elected':datetime.datetime.strptime(textchunk.text.strip(), '%d/%m/%Y').date()})
                except ValueError:
                    print "Hit the Poulett, John, 1st Earl Poulett or the Seligman, Charles Gabriel exception"
                    Fellow.update({'Elected':datetime.datetime.strptime(textchunk.text.strip()[0:10], '%d/%m/%Y').date()}) 
                # print Fellow
                # Little kludge to handle 1st Baron Adrian
                if Fellow['Name']=="Adrian, Edgar Douglas, 1":
                    Fellow['Name']=="Adrian, Edgar Douglas, 1st Baron Adrian of Cambridge"
                if Fellow.has_key('LifeSpan'):
                    part=Fellow['LifeSpan'].split('-')
                    if len(part)==1:
                        print "Trying to split lifespan with by en dash"
                        part=Fellow['LifeSpan'].split(u"\u2013")
                        if len(part)==1:    
                            print "Lifespan only has one part: ",part
                            part.append('')
                    #We should have two parts to parse to date here but they may not work
                    
                    Fellow.update({'Born':parseLifeSpan(part[0].strip()),'Died':parseLifeSpan(part[1].strip())})
                scraperwiki.sqlite.save(unique_keys=["Name"],data=Fellow, table_name="RoyalSocietyFellows")
                # print Fellow
        else:
            #For some reason
            #Should save the unexpected text into a table unless it is zero length
            if textchunk.text is not None and not textchunk.text.isspace():
                print "Text in an unexpected place: %s" % textchunk.text
                Unexpected={"ID":UnknownID,"Text":textchunk.text,"Page":page.attrib.get("number"),"left":leftcoord}
                scraperwiki.sqlite.save(unique_keys=["ID"],data=Unexpected, table_name="UnexpectedText")
                UnknownID=UnknownID+1import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser
import datetime

# Royal society fellows scraper,
# Source is:
# http://royalsociety.org/uploadedFiles/Royal_Society_Content/about-us/fellowship/Fellows1660-2007.pdf
# Ignore the front page saying A-J, the whole list is in there
# p5 start of records proper
# p195-198 are a second frontpiece
# p199-formated differently?
# We're going to use pdftoxml:
# http://linux.die.net/man/1/pdftohtml
# Some examples:
# https://scraperwiki.com/views/pdf_to_html_preview_4/edit/
# https://scraperwiki.com/scrapers/new/python?template=advanced-scraping-pdfs
#

# Most lifespans are separated by - but some are separated by en dash \u2013 and some are just "flourished" denoted by fl and a single year
# Wollaston was only president for less than a year so his PRS field is different from the rest
# Successful run should produce 8019 fellows.
# Parsing lifespan dates but only if they strictly conform to %d %B %Y format
# https://scraperwiki.com/docs/python/python_time_guide/ 
# Ian Hopkinson (9/12/12)

# Borrowed from Thomas Levine's blog post on handling exceptions
def parseLifeSpan(source):
    try:
         cleandate = datetime.datetime.strptime(source.strip(), '%d %B %Y')
    except ValueError:
         cleandate = None

    return cleandate

url = "http://royalsociety.org/uploadedFiles/Royal_Society_Content/about-us/fellowship/Fellows1660-2007.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

# Page 5 is the first one to contain useful stuff
# options="-f 5 -l 20"
options="-f 5"
# options="-f 108 -l 140"

ResumeAtPage = 4
xmldata = scraperwiki.pdftoxml(pdfdata,options)

print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 11000 characters are: ", xmldata[:11000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)
UnknownID=1

for page in pages:
    pagenumber=int(page.attrib.get("number"))
    if pagenumber < ResumeAtPage:
        print "Skipping page %d, before ResumeAtPage" % pagenumber
        continue 
    if pagenumber>194 and pagenumber<199:
        print "Skipping page %d because it is frontmatter:" % pagenumber
        continue
    print "Processing page: ", pagenumber
# Don't appear to get styling info (i.e. bold)
# Fellow names have left="135" tag
# Lifespan string have left="188" tag (but alias info also appears here- ther can be more than one - see Anglesey) (one appears at 193 on p117)
# Fellow class has left="560" except after p199 when it is "540"
# Election Date has left="661" except after p199 when it is "648" 
# President has indicative text in fellow class column on same line as name (fellow is on following line)
# Wierd stuff on George II-IV "Royal Fellow; Patron 1820 18/05/1820" (appears at 496 or 518)
    if pagenumber>198:
        FellowClassCol=540
        ElectionDateCol=648
    else:
        FellowClassCol=560
        ElectionDateCol=661

    #print FellowClassCol, ElectionDateCol

    for textchunk in (page is not None and page.xpath('text')):
        leftcoord = int(textchunk.attrib.get('left'))
        if leftcoord==135: #Get a FellowName this is the restart signal
            if textchunk.text is not None and not textchunk.text.isspace():
                Fellow={}
                Fellow={'Name':textchunk.text.strip()}
        elif leftcoord>187 and leftcoord<200: #Get a lifespan string - if this is a see... then we need to write an alias
            if textchunk.text is not None and not textchunk.text.isspace():
                if textchunk.text[0:3]=="See":
                    AliasRecord={'Name':Fellow['Name'],'Alias':textchunk.text[4:].strip()}
                    scraperwiki.sqlite.save(unique_keys=["Name"],data=AliasRecord, table_name="RoyalSocietyFellowAliases")
                    # print '''It's an alias!'''
                else:
                    Fellow.update({'LifeSpan':textchunk.text.strip()})
        elif leftcoord>495 and leftcoord<570: #Get a Fellow class - need to handle presidents here Atiyah is the first
            if textchunk.text is not None and not textchunk.text.isspace():
                if textchunk.text[0:3]=="PRS":
                    #Fellow.update({'President':textchunk.text[4:].strip()})
                    part=textchunk.text[4:].split('-')
                    if len(part)==2:
                        #Fellow.update({'StartPresident':part[0].strip()})
                        #Fellow.update({'EndPresident':part[1].strip()})
                        print Fellow
                        Fellow.update({'StartPresident':datetime.datetime.strptime(part[0].strip(), '%Y').date()})
                        # At the time of publication Robert May was President, this handles the "open" end of his presidency 
                        try:
                            Fellow.update({'EndPresident':datetime.datetime.strptime(part[1].strip(), '%Y').date()})
                        except ValueError:
                            print "Handling Robert May as an exception"
                    else:
                        # Wollaston was only President for 1 year
                        # Fellow.update({'StartPresident':part[0].strip()})
                        Fellow.update({'StartPresident':datetime.datetime.strptime(part[0].strip(), '%Y').date()})
                    print "President"
                    print Fellow
                else:
                    #Fellow.update({'President':' '})
                    Fellow.update({'Class':textchunk.text.strip()})
        elif leftcoord>640: #Get a Fellow election date, get one of these and we should write the set to a structure or maybe the SQL store
            if textchunk.text is not None and not textchunk.text.isspace():
                # Handle another exception, this is the elected date for Gordon Henry Dixon, it's either 1978. 
                if textchunk.text.strip()=='16/03/197':
                     textchunk.text='16/03/1978'
                # Another exception Poulett, John, 1st Earl Poulett - seems to have two election dates separated by a ;
                try:
                    Fellow.update({'Elected':datetime.datetime.strptime(textchunk.text.strip(), '%d/%m/%Y').date()})
                except ValueError:
                    print "Hit the Poulett, John, 1st Earl Poulett or the Seligman, Charles Gabriel exception"
                    Fellow.update({'Elected':datetime.datetime.strptime(textchunk.text.strip()[0:10], '%d/%m/%Y').date()}) 
                # print Fellow
                # Little kludge to handle 1st Baron Adrian
                if Fellow['Name']=="Adrian, Edgar Douglas, 1":
                    Fellow['Name']=="Adrian, Edgar Douglas, 1st Baron Adrian of Cambridge"
                if Fellow.has_key('LifeSpan'):
                    part=Fellow['LifeSpan'].split('-')
                    if len(part)==1:
                        print "Trying to split lifespan with by en dash"
                        part=Fellow['LifeSpan'].split(u"\u2013")
                        if len(part)==1:    
                            print "Lifespan only has one part: ",part
                            part.append('')
                    #We should have two parts to parse to date here but they may not work
                    
                    Fellow.update({'Born':parseLifeSpan(part[0].strip()),'Died':parseLifeSpan(part[1].strip())})
                scraperwiki.sqlite.save(unique_keys=["Name"],data=Fellow, table_name="RoyalSocietyFellows")
                # print Fellow
        else:
            #For some reason
            #Should save the unexpected text into a table unless it is zero length
            if textchunk.text is not None and not textchunk.text.isspace():
                print "Text in an unexpected place: %s" % textchunk.text
                Unexpected={"ID":UnknownID,"Text":textchunk.text,"Page":page.attrib.get("number"),"left":leftcoord}
                scraperwiki.sqlite.save(unique_keys=["ID"],data=Unexpected, table_name="UnexpectedText")
                UnknownID=UnknownID+1