import scraperwiki,urllib2,lxml.html

# Blank Python

url='http://www.chegg.com/search/tipler/'

def clean(fragment):
    return fragment.text_content().replace('\n','').replace('\t','').replace(u'\xa0',' ')

def scrapechegg(url):
    builder=[]
    prices=[]
    html=urllib2.urlopen(url).read() # get page
    root=lxml.html.fromstring(html)  # load into LXML

    for result in root.cssselect("div[class='search-result']"):     # for each of the search results,
        details=result.cssselect("table[class='book-details']")[0]  # grab the individual sections with price/metadata in
        pricebox=result.cssselect("td[class='price-box-cell']")[0]

        data={'ISBN':'', 'eISBN':''}
        for i,tr in enumerate(details.cssselect("tr")):             # go through each of the elements in the metadata
            text=clean(tr)                                          # and extract them via key:value or the fact that 
            if i==0:                                                # the first item's the title of the book
                data['title']=text
            else:
                (cat,colon,info)=text.partition(':')
                data[cat.replace('(','').replace(')','')]=info
        # build up a list to send to the datastore
            builder.append(data)   
            
        for p in pricebox.cssselect("input[type='hidden']"):   ### THIS DOESN'T WORK FOR ALL BOOKS/PRICES
            price={'ISBN':'','eISBN':''}                         # but it's similar to the above, only less neat
            if 'price' in p.keys():                              # because we only want some columns
                try:                                             # and works using HTML attributes.
                    price['ISBN']=p.attrib['isbn']               # Sadly, the tag we're looking for don't exist
                except KeyError:                                 # for some books. :(
                    pass
                try:
                    price['eISBN']=p.attrib['eisbn']
                except KeyError:
                    pass
                price['CLASS']=p.attrib['class']
                price['PRICE']=p.attrib['price']
                prices.append(price)
        
    # throw at datastore
    scraperwiki.sqlite.save(table_name='metadata',data=builder,unique_keys=['ISBN','eISBN'])
    scraperwiki.sqlite.save(table_name='prices',data=prices,unique_keys=['ISBN','eISBN','CLASS'])
        

scrapechegg(url)
