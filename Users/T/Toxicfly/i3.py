import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("http://dl.dropbox.com/u/87106626/Scrap/3.csv")


line = 0
import csv
reader = csv.reader(data.splitlines())
#headerline = reader.next()
for row in reader:
          
    try:
      html1 = scraperwiki.scrape(row[0])
      Ar6 = html1.split('<h4 class="oursku">');
      Tr6 = Ar6[1];
      Kr6 = Tr6.split('</h4>');
      SKU = Kr6[0].replace('Our SKU:','')
    except:
      SKU = ''


    try: 
     ImgU = row[0].split('/')
     x = len(ImgU)
     
     ImgF = ImgU[x-1].replace('p','')
     
     URL = 'http://www.build.com/index.cfm?page=product:mediaGallery&uniqueId='+str(ImgF)
     
     html = scraperwiki.scrape(URL)
     
     Arr = html.split('Large</a>')
     l=  len(Arr)
     for c in range(0,l-1):
      ArrX=Arr[c].split('onClick="loadImage(')
      z=len(ArrX)
      Tan =  ArrX[z-1]
      Fin = Tan.split(');')
      FinIma = 'http://www.build.com'+Fin[0].replace("'",'')
      data = [{'SKU':SKU, 'ImageURL':FinIma } ]

      scraperwiki.sqlite.save(unique_keys=["ImageURL"], data=data)
      #print 'http://www.build.com'+Fin[0].replace("'",'')
    except:
     html = ''

