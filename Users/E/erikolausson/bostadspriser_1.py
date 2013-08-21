import scraperwiki

# Blank Python

from mechanize import Browser
import mechanize
import lxml.html
count = 2
radnr = 0
next_page = "http://www.hemnet.se/resultat?page="+str(count)
br = Browser()
br.set_handle_robots(False)

br.open("http://www.hemnet.se/sok/avancerad", timeout=300.0)

br.select_form(nr=0) #only one form to choose from on page br.form now points to list of controls (checkboxes etc.) on page

br.form.find_control("search[municipality_ids][]").items[141].selected=True #check the Malmö checkbox
br.form.find_control("search[item_types][]").items[0].selected=False #uncheck the "search all" checkbox
br.form.find_control("search[item_types][]").items[6].selected=True #check the Bostadsrätt checkbox
br.form.controls[7].items[0].selected=False #uncheck box "nybyggt"
br.form.controls[13].items[0].selected=False #uncheck box "radhus"

br.form.find_control("search[fee_max]").value="10000" #set maximum månadsavgift till 10.000 kronor 
br.form.find_control("search[price_per_m2_min]").value="1000" #set minimum price per sq. meter to 1.000 kronor to avoid appartments without defined prices or areas   
print "så här långt"

response = br.submit()
#print response.read()
#forms = mechanize.ParseFile(br, "http://www.hemnet.se/sok/avancerad", backwards_compat=False)
#form = forms[0]

#print form

#html = scraperwiki.scrape("http://www.hemnet.se/sok/avancerad")

root = lxml.html.fromstring(response.read())
#root2.lxml.html.fromstring(response2.read())
#print "root före", root
pris= root.cssselect("ul#search-results li.price-per-m2")
#print "root efter", root
adress = root.cssselect("ul#search-results li.address")
#print adress

#pris = lgh.cssselect("il.price-per-m2")
#print lgh
for h in range(len(pris)):
    print pris[h].text_content()
    print adress[h].text_content()
    radnr = radnr+1    
    scraperwiki.sqlite.save(unique_keys=["row"], data={"row":radnr, "adress":adress[h].text_content(), "pris":pris[h].text_content()}) 

#print next_page

while br.open(next_page):
    count = count+1
    next_page = "http://www.hemnet.se/resultat?page="+str(count)
    print next_page
    response = br.open(next_page)
    
    root = lxml.html.fromstring(response.read())
    #root2.lxml.html.fromstring(response2.read())
    #print "root före", root
    pris= root.cssselect("ul#search-results li.price-per-m2")
    #print "root efter", root
    adress = root.cssselect("ul#search-results li.address")
    #print adress
    for h in range(len(pris)):
        print pris[h].text_content()
        print adress[h].text_content()
        radnr = radnr+1   
        scraperwiki.sqlite.save(unique_keys=["row"], data={"row":radnr, "adress":adress[h].text, "pris":pris[h].text}) 

#print "första", lgh[0].text_content()
#print lgh
#print "andra", lgh[5].text_content()

#print "tredje", lgh[7].text_content()

#print lgh

#nice_links = [l for l in br.links()] #returns list of  all links on page

#print nice_links


#root = lxml.html.fromstring(br.read())

#<div class=" multiselectinput municipality-ids-post form-post">
