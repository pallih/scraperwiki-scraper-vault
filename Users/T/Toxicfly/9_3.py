import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("http://dl.dropbox.com/u/87106626/Scrap/9.csv")

line = 0
import csv
reader = csv.reader(data.splitlines())
#headerline = reader.next()
for row in reader:
 try:
  for page in range(1,2):
     
 
     html = scraperwiki.scrape(row[0])
          
     try:
      Ar = html.split('<title>');
      Tr = Ar[1];
      Kr = Tr.split('</title>');
      Name = Kr[0]
     except IndexError:
      Name = ''
     
     try:
      Ar1 = html.split('<link rel="canonical" href=');
      Tr1 = Ar1[1];
      Kr1 = Tr1.split('"/>');
      URL = Kr1[0]
     except IndexError:
      URL = ''
     
     try:
      Ar2 = html.split('<meta name="description" content="');
      Tr2 = Ar2[1];
      Kr2 = Tr2.split('/>');
      SDesc = Kr2[0]
     except IndexError:
      SDesc = ''
     
     
     try:
      Ar3 = html.split('<meta property="og:image" content="');
      Tr3 = Ar3[1];
      Kr3 = Tr3.split('/>');
      ImageURL = Kr3[0]
     except IndexError:
      ImageURL = ''
     
     try:
      Ar4 = html.split('<div class="productDescriptionOver content">');
      Tr4 = Ar4[1];
      Kr4 = Tr4.split('</div>');
      LDesc = Kr4[0]
     except IndexError:
      LDesc = ''
     

     try:
      Ar5 = html.split('<div class="price ">');
      Tr5 = Ar5[1];
      Kr5 = Tr5.split('</div>');
      Price = Kr5[0]
     except IndexError:
      Price = ''
     
     
     try:
      Ar6 = html.split('<h4 class="oursku">');
      Tr6 = Ar6[1];
      Kr6 = Tr6.split('</h4>');
      SKU = Kr6[0]
     except IndexError:
      SKU = ''
     

     try:
      Ar7 = html.split('needsConfig');
      Tr7 = Ar7[1];
      Kr7 = Tr7.split('$get');
      Variant = Kr7[0]
     except IndexError:
      Variant = ''
     
     try:
      Ar8 = html.split('s.hier1="');
      Tr8 = Ar8[1];
      Kr8 = Tr8.split('";');
      Hier = Kr8[0]
     except IndexError:
      Hier = ''

     data = [{'SKU':SKU, 'Title':Name, 'URL':row[0], 'ShortDesc':SDesc , 'LongDesc':LDesc , 'ImageURL':ImageURL, 'Price':Price,'Variant':Variant,'Hierarchy':Hier } ]

     scraperwiki.sqlite.save(unique_keys=["SKU"], data=data)


 except:
  HTML = ''