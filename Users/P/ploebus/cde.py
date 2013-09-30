###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki



# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
# Scraper for the UK Employment Appeal Tribunal

# FIXME: remove excess tabs/newlines from fields, particularly dates and appeal nos.

import urllib, urllib2
import cookielib
import lxml.html
import datetime
import urlparse
import scraperwiki


def getFields(tr):
    returnArr=[]
    ths=tr.cssselect('th')
    for th in ths:
        #print th.text_content()
        returnArr.append("`"+ th.text_content()+ "` string")
   
    theString=','.join(returnArr)
    print theString
    scraperwiki.sqlite.execute("create table OUSD(" + theString + ")")
    return returnArr
        
def getJudgments(root):
    
    myTables=root.cssselect("table")
    trs=myTables[0].cssselect("tr")
   
    
    #field_names=getFields(trs[0])
    
    i=0

    for tr in trs:
        tds=tr.cssselect("td")
        
        fields = [str(td.text_content()).rstrip() for td in tds]
            #fields.append(str(td.text_content()))
             
        insertString=','.join(fields)
        insertString.replace(u'\xa0',"")
        print insertString
        try: 
            scraperwiki.sqlite.execute("insert into OUSD values (" + insertString + ")")
        except:
            print 'no luck'
            continue
        else:
            scraperwiki.sqlite.commit
        
        #data = dict(zip(field_names, fields))
        #print data
    i=i+1
        #scraperwiki.sqlite.save(unique_keys=['id'], data=data)

field_names=[]
html = scraperwiki.scrape('http://dq.cde.ca.gov/dataquest/Cbeds3.asp?Tp=on&GradeSpan=on&NumSchls=on&puplTeach=on&FreeLunch=on&SEEnroll=on&Enroll=on&PctEL=on&PctFEP=on&PctRe=on&Grads=on&Uccsu=on&NumDrops=on&Drop1yr=on&Drop4yr=on&FTEAdmin=on&FTEPupil=on&FTETeach=on&Cl=on&CompNum=on&Int=on&StarLang1=on&StarLang2=on&StarMath1=on&StarMath2=on&StarSci1=on&StarSci2=on&StarSci3=on&StarSci4=on&StarSoc1=on&StarSoc2=on&cSelect=0161259--OAKLAND+UNIFIED&cChoice=DstProf2&cYear=2009-10&cLevel=District&cTopic=Profile&myTimeFrame=S&submit1=Submit')
root = lxml.html.fromstring(html)
getJudgments(root)



###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki



# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

import lxml.html
# Scraper for the UK Employment Appeal Tribunal

# FIXME: remove excess tabs/newlines from fields, particularly dates and appeal nos.

import urllib, urllib2
import cookielib
import lxml.html
import datetime
import urlparse
import scraperwiki


def getFields(tr):
    returnArr=[]
    ths=tr.cssselect('th')
    for th in ths:
        #print th.text_content()
        returnArr.append("`"+ th.text_content()+ "` string")
   
    theString=','.join(returnArr)
    print theString
    scraperwiki.sqlite.execute("create table OUSD(" + theString + ")")
    return returnArr
        
def getJudgments(root):
    
    myTables=root.cssselect("table")
    trs=myTables[0].cssselect("tr")
   
    
    #field_names=getFields(trs[0])
    
    i=0

    for tr in trs:
        tds=tr.cssselect("td")
        
        fields = [str(td.text_content()).rstrip() for td in tds]
            #fields.append(str(td.text_content()))
             
        insertString=','.join(fields)
        insertString.replace(u'\xa0',"")
        print insertString
        try: 
            scraperwiki.sqlite.execute("insert into OUSD values (" + insertString + ")")
        except:
            print 'no luck'
            continue
        else:
            scraperwiki.sqlite.commit
        
        #data = dict(zip(field_names, fields))
        #print data
    i=i+1
        #scraperwiki.sqlite.save(unique_keys=['id'], data=data)

field_names=[]
html = scraperwiki.scrape('http://dq.cde.ca.gov/dataquest/Cbeds3.asp?Tp=on&GradeSpan=on&NumSchls=on&puplTeach=on&FreeLunch=on&SEEnroll=on&Enroll=on&PctEL=on&PctFEP=on&PctRe=on&Grads=on&Uccsu=on&NumDrops=on&Drop1yr=on&Drop4yr=on&FTEAdmin=on&FTEPupil=on&FTETeach=on&Cl=on&CompNum=on&Int=on&StarLang1=on&StarLang2=on&StarMath1=on&StarMath2=on&StarSci1=on&StarSci2=on&StarSci3=on&StarSci4=on&StarSoc1=on&StarSoc2=on&cSelect=0161259--OAKLAND+UNIFIED&cChoice=DstProf2&cYear=2009-10&cLevel=District&cTopic=Profile&myTimeFrame=S&submit1=Submit')
root = lxml.html.fromstring(html)
getJudgments(root)



