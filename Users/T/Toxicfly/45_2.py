import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/Apps.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:

     URL = row[0]
     print URL
     html = scraperwiki.scrape(URL)
     print html
     try:
      Ar = html.split('<h5>Released</h5>');
      Tr = Ar[1];
      Kr = Tr.split('</strong>');
      Released = Kr[0]
     except IndexError:
      Released = ''
     
     try:
      Ar1 = html.split('App by');
      Tr1 = Ar1[1];
      Kr1 = Tr1.split('</p>');
      AppBy = Kr1[0]
     except IndexError:
      AppBy = ''
     
     try:
      Ar2 = html.split('DetailOverviewTabComp:priceInfo" class="multi-line-to-fix">');
      Tr2 = Ar2[1];
      Kr2 = Tr2.split('</span>');
      Pricing = Kr2[0]
     except IndexError:
      Pricing = ''
     
     
     try:
      Ar3 = html.split('<h5>Categories</h5>');
      Tr3 = Ar3[1];
      Kr3 = Tr3.split('</p>');
      Cat = Kr3[0]
     except IndexError:
      Cat = ''
     
     try:
      Ar4 = html.split('<p class="h1-tagline" id="listingTagLine">');
      Tr4 = Ar4[1];
      Kr4 = Tr4.split('</p>');
      TagLine = Kr4[0]
     except IndexError:
      TagLine = ''
     

     try:
      Ar5 = html.split('onclick="initializeLeadPanel(''Demo'');">');
      Tr5 = Ar5[1];
      Kr5 = Tr5.split('</a>');
      Demo = Kr5[0]
     except IndexError:
      Demo = ''
     
     
     try:
      Ar6 = html.split('onclick="initializeLeadPanel(''Test Drive'');">');
      Tr6 = Ar6[1];
      Kr6 = Tr6.split('</a>');
      TestDrive = Kr6[0]
     except IndexError:
      TestDrive = ''
     

     try:
      Ar7 = html.split('<title>');
      Tr7 = Ar7[1];
      Kr7 = Tr7.split('</title>');
      Title = Kr7[0]
     except IndexError:
      Title = ''
     
     try:
      Ar8 = html.split('class="rating-amount">');
      Tr8 = Ar8[1];
      Kr8 = Tr8.split('</span>');
      NoRating = Kr8[0]
     except IndexError:
      NoRating = ''

     data = [{'Title':Title, 'TagLine':TagLine, 'URL':row[0], 'Released':Released , 'AppBy':AppBy , 'Pricing':Pricing, 'Cat':Cat,'Demo':Demo,'TestDrive':TestDrive,'Ratings Number':NoRating } ]

     scraperwiki.sqlite.save(unique_keys=["URL"], data=data)

