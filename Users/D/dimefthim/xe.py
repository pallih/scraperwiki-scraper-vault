import BeautifulSoup, scraperwiki, datetime

scraperwiki.metadata.save('data_columns', ['id', 'date', 'Περιοχή', 'r_price' 'Είδος', 'Εμβαδόν', 'Όροφος', 'Έτος κατασκευής', 'Υπνοδωμάτια', 'Μπάνια', 'Πάρκιν', 'Είδος πάρκιν', 'Αυτόνομη θέρμανση', 'Με αποθήκη', 'Τζάκι', 'Ηλιακός θερμοσίφωνας', 'ΦΑ' ])

city = 'γαλατσι'

fundaUrl = 'http://www.property.gr'

startUrl = fundaUrl + '/πωλήσεις/κατοικιες/' + city 


html = scraperwiki.scrape(startUrl)
soup = BeautifulSoup.BeautifulSoup(html)

# get number of pages
pages = soup.findAll(attrs={'class' : 'page'})


items = []
today = datetime.date.today()

#for pageNo in range(1, 1 + 1):
 
#    nextUrl = startUrl + '?page=' + str(pageNo)
#    print 'page: ' + nextUrl
#    html = scraperwiki.scrape(nextUrl)
 #   soup = BeautifulSoup.BeautifulSoup(html)
 
 

     for ul in soup.findAll('ul', 'r_stats'):
         realItem = {'date' : today}

        for r_price in ul.findAll('li', 'r_price'):
             realItem['r_price'] = r_price.string.replace ('&euro;', '').strip().replace('.','')


        
        items.append(realItem)
        scraperwiki.datastore.save(unique_keys=['id'], data=realItem)
        print 'items saved: ' + str(len(items))



