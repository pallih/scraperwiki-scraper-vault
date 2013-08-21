import scraperwiki
from BeautifulSoup import BeautifulSoup

unknown=0

starting_url = 'http://www.buzzle.com/articles/list-of-disney-movies.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)



count=0
blanks=0
table = soup.findAll('table')
for table in table:
    for attr,val in table.attrs:
        
        if attr=='summary':
            print val
            ccode=val.split(' ')[0]
            ctitle=val.replace(ccode,'').strip()
    firstrow = True
    

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
            

            unknown+=1

             
            count +=1
            
    
            # save records to the datastore
           
        else:
            firstrow=False

print count
print unknown,blanks



