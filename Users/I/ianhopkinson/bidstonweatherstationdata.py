import scraperwiki
import urllib2
import lxml.etree
import datetime

# Bidston Weather Station Data
# Ian Hopkinson (31/12/12)

# TODO Parse the parent page to find all the available PDFs
# Multiple datasets, this one is for pressure:
url = "http://www.pol.ac.uk/appl/hist_met/pressure.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

# Put options here if we need them
options=''
#options="-f 5 -l 5"
xmldata = scraperwiki.pdftoxml(pdfdata,options)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The xml file looks like this: ", xmldata
    
root = lxml.etree.fromstring(xmldata)
pages = list(root)


for page in pages:
    CentresArr=[]
    pagenumber=int(page.attrib.get("number"))
    #if pagenumber>1:
    #    break
    print "Processing page number: ",pagenumber
    for textchunk in (page is not None and page.xpath('text')):
        # print textchunk
        leftcoord = int(textchunk.attrib.get('left'))
        width = int(textchunk.attrib.get('width'))
        topcoord = int(textchunk.attrib.get('top'))
        if topcoord == 156:
            for child in textchunk:
                # print "%s column at left = %d" %(child.text, leftcoord)
                #Calculate column centre
                # CentresDict[child.text]=leftcoord+width/2
                CentresArr.append(leftcoord+width/2)
        #print textchunk.text
        if leftcoord == 120:
            for child in textchunk:
                #print "%s row at top = %d" %(child.text, leftcoord)
                CurrentYear=int(child.text)
        
        if leftcoord != 120 and topcoord!=156:           
            # Use CentresList to get closest colum centre
            tmp=[]
            # TODO I should probably use "Map" here
            for items in CentresArr:
                #print float(items)-float((leftcoord+width/2))
                tmp.append(abs(float(items)-float((leftcoord+width/2))))
            CurrentMonth=tmp.index(min(tmp))+1
            # TODO Don't currently handle non-month entries such as "Mean" - could make a good validation step
            if CurrentMonth<13:
                date=datetime.date(CurrentYear, CurrentMonth,1)
                try:
                    record={"date":date,"Pressure":float(textchunk.text)}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                except ValueError:
                    # TODO for some reasons there is a glitch which puts two pressures into one string, need to split numbers and put into successive cells
                    if textchunk.text=="NR":
                        print "Hit an NR for Year %d, Month %d" % (CurrentYear,CurrentMonth)
                        continue
                    SplitPressures=textchunk.text.split() 
                    date=datetime.date(CurrentYear, CurrentMonth,1)
                    record={"date":date,"Pressure":float(SplitPressures[0])}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                    date=datetime.date(CurrentYear, CurrentMonth+1,1)
                    record={"date":date,"Pressure":float(SplitPressures[1])}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                    print "Double value handled for Year %d, Month %d, string = %s" % (CurrentYear,CurrentMonth,textchunk.text)
                except TypeError:
                    # TODO Suspect this is picking up the page titles, which are in bold
                    for child in textchunk:
                        print "This should be the page title: ", child.text
                    #print "Type error for Year %d, Month %d, string = %s" % (CurrentYear,CurrentMonth,textchunk.text)
print CentresArr
print tmp

import scraperwiki
import urllib2
import lxml.etree
import datetime

# Bidston Weather Station Data
# Ian Hopkinson (31/12/12)

# TODO Parse the parent page to find all the available PDFs
# Multiple datasets, this one is for pressure:
url = "http://www.pol.ac.uk/appl/hist_met/pressure.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

# Put options here if we need them
options=''
#options="-f 5 -l 5"
xmldata = scraperwiki.pdftoxml(pdfdata,options)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The xml file looks like this: ", xmldata
    
root = lxml.etree.fromstring(xmldata)
pages = list(root)


for page in pages:
    CentresArr=[]
    pagenumber=int(page.attrib.get("number"))
    #if pagenumber>1:
    #    break
    print "Processing page number: ",pagenumber
    for textchunk in (page is not None and page.xpath('text')):
        # print textchunk
        leftcoord = int(textchunk.attrib.get('left'))
        width = int(textchunk.attrib.get('width'))
        topcoord = int(textchunk.attrib.get('top'))
        if topcoord == 156:
            for child in textchunk:
                # print "%s column at left = %d" %(child.text, leftcoord)
                #Calculate column centre
                # CentresDict[child.text]=leftcoord+width/2
                CentresArr.append(leftcoord+width/2)
        #print textchunk.text
        if leftcoord == 120:
            for child in textchunk:
                #print "%s row at top = %d" %(child.text, leftcoord)
                CurrentYear=int(child.text)
        
        if leftcoord != 120 and topcoord!=156:           
            # Use CentresList to get closest colum centre
            tmp=[]
            # TODO I should probably use "Map" here
            for items in CentresArr:
                #print float(items)-float((leftcoord+width/2))
                tmp.append(abs(float(items)-float((leftcoord+width/2))))
            CurrentMonth=tmp.index(min(tmp))+1
            # TODO Don't currently handle non-month entries such as "Mean" - could make a good validation step
            if CurrentMonth<13:
                date=datetime.date(CurrentYear, CurrentMonth,1)
                try:
                    record={"date":date,"Pressure":float(textchunk.text)}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                except ValueError:
                    # TODO for some reasons there is a glitch which puts two pressures into one string, need to split numbers and put into successive cells
                    if textchunk.text=="NR":
                        print "Hit an NR for Year %d, Month %d" % (CurrentYear,CurrentMonth)
                        continue
                    SplitPressures=textchunk.text.split() 
                    date=datetime.date(CurrentYear, CurrentMonth,1)
                    record={"date":date,"Pressure":float(SplitPressures[0])}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                    date=datetime.date(CurrentYear, CurrentMonth+1,1)
                    record={"date":date,"Pressure":float(SplitPressures[1])}
                    scraperwiki.sqlite.save(unique_keys=["date"],data=record)
                    print "Double value handled for Year %d, Month %d, string = %s" % (CurrentYear,CurrentMonth,textchunk.text)
                except TypeError:
                    # TODO Suspect this is picking up the page titles, which are in bold
                    for child in textchunk:
                        print "This should be the page title: ", child.text
                    #print "Type error for Year %d, Month %d, string = %s" % (CurrentYear,CurrentMonth,textchunk.text)
print CentresArr
print tmp

