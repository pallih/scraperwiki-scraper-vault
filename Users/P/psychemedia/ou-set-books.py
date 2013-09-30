###############################################################################
# Basic scraper
###############################################################################
import scraperwiki
from BeautifulSoup import BeautifulSoup

unknown=0
# retrieve a page
starting_url = 'http://www3.open.ac.uk/about/setbooks/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# The books for each course are listed in a separate table
# use BeautifulSoup to get all <table> tags
count=0
blanks=0
tables = soup.findAll('table') 
for table in tables:
    for attr,val in table.attrs:
        # The course code and course title are contained in the table summary attribute
        if attr=='summary':
            print val
            ccode=val.split(' ')[0]
            ctitle=val.replace(ccode,'').strip()
    firstrow = True
    
    # Work through each row in the table - one row per book - ignoring the header row
    for row in table.findAll('tr'):
        blankLine=False
        for attr,val in row.attrs:
            if attr=='class' and val=='white':
                blankLine=True
                blanks+=1
        if blankLine:
            break
        if not firstrow:
            cells=row.findAll('td')
            print cells
            author=cells[0].text.replace('&nbsp;','')
            author=author.replace('&amp;','and')
            title=cells[1].text
            isbn=cells[2].text
            isbn=isbn.replace('&nbsp;','')
            publisher=cells[3].text
            publisher=publisher.replace('&nbsp;','')
            rrp=cells[4].text.replace('&#163;','')
            print ccode, ctitle,author,title,isbn,publisher,rrp
            if isbn=='':
                key=ccode+'_unkown:'+str(unknown)
                unknown+=1
            else:
                key=ccode+'_'+isbn
            count +=1
            record = {'id':key, 'Course Code':ccode, 'Course title':ctitle,'Author':author,'Title':title,'ISBN':isbn,'Publisher':publisher,'RRP':rrp }
    
            # save records to the datastore
            scraperwiki.datastore.save(['id'], record)
        else:
            firstrow=False

print count
print unknown,blanks###############################################################################
# Basic scraper
###############################################################################
import scraperwiki
from BeautifulSoup import BeautifulSoup

unknown=0
# retrieve a page
starting_url = 'http://www3.open.ac.uk/about/setbooks/'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# The books for each course are listed in a separate table
# use BeautifulSoup to get all <table> tags
count=0
blanks=0
tables = soup.findAll('table') 
for table in tables:
    for attr,val in table.attrs:
        # The course code and course title are contained in the table summary attribute
        if attr=='summary':
            print val
            ccode=val.split(' ')[0]
            ctitle=val.replace(ccode,'').strip()
    firstrow = True
    
    # Work through each row in the table - one row per book - ignoring the header row
    for row in table.findAll('tr'):
        blankLine=False
        for attr,val in row.attrs:
            if attr=='class' and val=='white':
                blankLine=True
                blanks+=1
        if blankLine:
            break
        if not firstrow:
            cells=row.findAll('td')
            print cells
            author=cells[0].text.replace('&nbsp;','')
            author=author.replace('&amp;','and')
            title=cells[1].text
            isbn=cells[2].text
            isbn=isbn.replace('&nbsp;','')
            publisher=cells[3].text
            publisher=publisher.replace('&nbsp;','')
            rrp=cells[4].text.replace('&#163;','')
            print ccode, ctitle,author,title,isbn,publisher,rrp
            if isbn=='':
                key=ccode+'_unkown:'+str(unknown)
                unknown+=1
            else:
                key=ccode+'_'+isbn
            count +=1
            record = {'id':key, 'Course Code':ccode, 'Course title':ctitle,'Author':author,'Title':title,'ISBN':isbn,'Publisher':publisher,'RRP':rrp }
    
            # save records to the datastore
            scraperwiki.datastore.save(['id'], record)
        else:
            firstrow=False

print count
print unknown,blanks