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
    for td in root.cssselect("table[id='ctl00_m_tblSC'] td"):#sometimes there are multiple contacts each with their own td
        if len(td.text)!=95:#exclude the title cell which has length 95            
            wholecell= lxml.html.tostring(td)
            reg = r'mailto:(.*)\@(.*)\"'
            match = re.search(reg, wholecell)
# You grab items by index. Starting from 1, 0 is the entire match
            if match:#a few entries have no email address so in the else section replace with "none"
                email = match.group(0)
                email = email[7:-1]#this removes mailto: and a trailing double quote
                print i, td.text, email
                scraperwiki.sqlite.execute("insert into contacts values (?,?,?)", (i, email, td.text))
                scraperwiki.sqlite.commit()
            else:
                print i, td.text
                scraperwiki.sqlite.execute("insert into contacts values (?,?,?)", (i, "none", td.text))
                scraperwiki.sqlite.commit()
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
    for td in root.cssselect("table[id='ctl00_m_tblSC'] td"):#sometimes there are multiple contacts each with their own td
        if len(td.text)!=95:#exclude the title cell which has length 95            
            wholecell= lxml.html.tostring(td)
            reg = r'mailto:(.*)\@(.*)\"'
            match = re.search(reg, wholecell)
# You grab items by index. Starting from 1, 0 is the entire match
            if match:#a few entries have no email address so in the else section replace with "none"
                email = match.group(0)
                email = email[7:-1]#this removes mailto: and a trailing double quote
                print i, td.text, email
                scraperwiki.sqlite.execute("insert into contacts values (?,?,?)", (i, email, td.text))
                scraperwiki.sqlite.commit()
            else:
                print i, td.text
                scraperwiki.sqlite.execute("insert into contacts values (?,?,?)", (i, "none", td.text))
                scraperwiki.sqlite.commit()
