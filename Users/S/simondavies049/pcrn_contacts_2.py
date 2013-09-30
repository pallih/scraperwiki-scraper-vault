import scraperwiki
import lxml.html
import re #regular expressions

#uncomment the following if there is no database yet - CAUTION: data will be appended likely causing duplication if the database is not cleared before the run
#scraperwiki.sqlite.execute("create table contacts(study string, `email` string, `contact` string)")#although study is +ve int, store as string in case ever has leading zero

#create an array of the study numbers you are interested in. This must be whole numbers separated by commas.
#it can be a long list and span multiple lines if needed. 

arr=["10330", "10123", "10456", "12831"]

#loop through the study numbers in the array and fetch the detail page for each one from the PCRN public website
for i in arr:
    html = scraperwiki.scrape("http://public.ukcrn.org.uk/Search/StudyDetail.aspx?StudyID=%s" %i)
    root = lxml.html.fromstring(html) 
    for td in root.cssselect("table[id='ctl00_hypDocumentation'] td"):#sometimes there are multiple contacts each with their own td
        #if len(td.text)=42:#hoping all the close date cells have this length            
        wholecell= lxml.html.tostring(td)
        print wholecell
import scraperwiki
import lxml.html
import re #regular expressions

#uncomment the following if there is no database yet - CAUTION: data will be appended likely causing duplication if the database is not cleared before the run
scraperwiki.sqlite.execute("create table contacts(study string, `email` string, `contact` string)")#although study is +ve int, store as string in case ever has leading zero

#create an array of the study numbers you are interested in. This must be whole numbers separated by commas.
#it can be a long list and span multiple lines if needed. 

arr=["10330", "10123", "10456", "12831"]

#loop through the study numbers in the array and fetch the detail page for each one from the PCRN public website
for i in arr:
    html = scraperwiki.scrape("http://public.ukcrn.org.uk/Search/StudyDetail.aspx?StudyID=%s" %i)
    root = lxml.html.fromstring(html) 
    for td in root.cssselect("table[id='ctl00_hypDocumentation'] td"):#sometimes there are multiple contacts each with their own td
        #if len(td.text)=42:#hoping all the close date cells have this length            
        wholecell= lxml.html.tostring(td)
        print wholecell
