import scraperwiki
import lxml.html

record={}

#create repeatable scraper routine, to do each page
def scrape_urls(html):
    root = lxml.html.fromstring(html)
    ax = root.cssselect('div.jr_tableview a') # get all the <a> tags
    for a in ax:
            s=a.attrib['href']
            if s.find("#") == -1:
                record['link']='http://www.whatstove.co.uk' + a.attrib['href']
                scraperwiki.sqlite.save(['link'], record, 'sourceurls')

#list of all pages to scrape:
urllist = [
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=2&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=3&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=4&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=5&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=6&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=7&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=8&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=9&query=any',
'http://www.whatstove.co.uk/advanced-stove-search/search-results/?criteria=2&jr_okforsmokelesszone=1&order=alpha&page=10&query=any'
];

for link in urllist:
    html=scraperwiki.scrape(link)
    scrape_urls(html)

urllist = scraperwiki.sqlite.select('''* from sourceurls''')

for l in urllist:
    url = l["link"]
    html=scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    record['link']=url

    dx = root.cssselect('div#maincolumn')[0] # get all the <div> tags

    # get heading
    try:
        h=dx.cssselect('h1.contentheading')[0]
        heading=h.cssselect('span.fn')[0]
        #print heading.text
        record['heading']=heading.text
    except :
        print "error"
        
    #get image
    try:
        i=dx.cssselect('div.itemMainImage img')[0]
        #print i.attrib['src']
        record['image']=i.attrib['src']
    except :
        print "error"
    
    #get flue diameter
    try:
        f=dx.cssselect('div."fieldRow jr_fluediam" div')[1]
        #print f.text
        record['fluesize']=f.text
    except :
        print "error"
    
    #get heat output
    try:
        f=dx.cssselect('div."fieldRow jr_heatoutput" div')[1]
        #print f.text
        record['output']=f.text
    except :
        print "error"
    
    #get fueltype
    try:
        f=dx.cssselect('div."fieldRow jr_fueltype" div')[1]
        fa=f.cssselect('a')[0]
        #print fa.text
        record['fueltype']=fa.text
    except :
        print "error"
    
    #get clenburn
    try:
        f=dx.cssselect('div."fieldRow jr_cleanburning" div')[1]
        fa=f.cssselect('a')[0]
        #print fa.text
        record['cleanburn']=fa.text
    except :
        print "error"
        
    #get airwash
    try:
        f=dx.cssselect('div."fieldRow jr_airwash" div')[1]
        record['airwash']=f.text
    except :
        print "error"
    
    #get efficiency
    try:
        f=dx.cssselect('div."fieldRow jr_efficiency" div')[1]
        record['efficiency']=f.text
    except :
        print "error"
    
    #get smokecontroll
    try:
        f=dx.cssselect('div."fieldRow jr_okforsmokelesszone" div')[1]
        record['smokecontroll']=f.text
    except :
        print "error"
    
    #get appearance
    try:
            f=dx.cssselect('div."fieldRow jr_appearance" div')[1]
            record['appearance']=f.text
    except :
            print "error"

    #get madeof
    try:
        f=dx.cssselect('div."fieldRow jr_madeof" div')[1]
        fa=f.cssselect('a')[0]
        record['madeof']=fa.text
    except :
        print "error"
    
    #get fuelexit
    try:
        f=dx.cssselect('div."fieldRow jr_flueexitpoint" div')[1]
        record['fuelexit']=f.text
    except :
        print "error"
    
    #get height
    try:
        f=dx.cssselect('div."fieldRow jr_height" div')[1]
        record['height']=f.text
    except :
        print "error"
    
    #get width
    try:
        f=dx.cssselect('div."fieldRow jr_width" div')[1]
        record['width']=f.text
    except :
        print "error"
    
    #get depth
    try:
        f=dx.cssselect('div."fieldRow jr_depth" div')[1]
        record['depth']=f.text
    except :
        print "error"
    
    scraperwiki.sqlite.save(['link'], record, 'defra_exempt_stoves')
    




    
    #get material
    #f=dx.cssselect('div."fieldRow jr_fluediam" div')[1]
    #fd=f.cssselect('div.fieldValue')[1]
    #print f.text
    #print fd.tail
    #print df.attrib['src']
    #print lxml.html.tostring(f)
    
    
    # if link.has_key('href'):




##dx = root.cssselect('div#maincolumn div') # get all the <div> tags
##for d in dx:
     #print lxml.html.tostring(d)
             #scraperwiki.sqlite.save(['link'], record) # save the records one by one

     #if d.attrib['class'] = "contentheading"
     #   print "heading"

     #elif d.attrib['class'] = "itemMainImage"
     #   print "image"
     ##print lxml.html.tostring(d.cssselect('div.itemMainImage')[0])
     #print d.attrib['class']
     #print lxml.html.tostring(d)
     
#scraperwiki.sqlite.save(['link'], record)

#for l in urllist:
#    url = l["link"]
#    html=scraperwiki.scrape(url)
#    root = lxml.html.fromstring(html)
#    record['link']=url
#    #record['data']=html
#    dx = root.cssselect('div.maincolumn div') # get all the <div> tags
#    for d in dx:
#             #print lxml.html.tostring(d)
#             #scraperwiki.sqlite.save(['link'], record) # save the records one by one
#        print d.attrib['class']
#            #if d.attrib['class']="contentheading"
#            #    record['heading']=lxml.html.tostring(d)
#            #elif d.attrib['class']="itemMainImage"
#            #    record['image']=lxml.html.tostring(d)
#
#    scraperwiki.sqlite.save(['link'], record)







#html=scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)
#print html

#sx=root.cssselect('h1.contentheading span')
#tit=root.cssselect('span.fn t')
#for t in tit
#    print t.text
#print sx
#for s in sx
#    #record = {}
#    if a.attrib['class'] = "fn" :
#        print s



