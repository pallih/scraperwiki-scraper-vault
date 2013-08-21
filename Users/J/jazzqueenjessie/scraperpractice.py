import scraperwiki
#html = scraperwiki.scrape("http://slo.craigslist.org/search/apa?zoomToPosting=&query=SLO&srchType=A&minAsk=&maxAsk=4000&bedrooms=3")
#print html

import lxml.etree
import lxml.html

# create an example case
html = """<html><body>
<p class="row" data-latitude="35.251171047748" data-longitude="-120.637810744352" data-pid="3810193234">
    <a href="/apa/3810193234.html" class="i" data-id="3K23M43N15N75Ef5K5d5g6b4c135a3ad81f13.jpg"></a>
    <span class="pl">
        <span class="star"></span>
        <small><span class="date">May 22</span></small>
        <a href="/apa/3810193234.html">3 bed / 2 bath SLO Home</a>
    </span>
    <span class="l2">
        <span class="pnr">
            <span class="price">$2400</span>
             / 3br - 1400ft&sup2; -  
            <span class="pp"></span><small> (San Luis Obispo)</small>
            <span class="px"><span class="p"> pic&nbsp;<a href="#" class="maptag" data-pid="3810193234">map</a></span></span>
         </span>
     </span>
</p>
  
<p class="row" data-pid="3798750481">
     <a href="/apa/3798750481.html" class="i"></a>
     <span class="pl">
         <span class="star"></span>
         <small> <span class="date">May 21</span></small>
         <a href="/apa/3798750481.html">Available July</a> </span>
         <span class="l2">
              <span class="pnr">
                  <span class="price">$1950</span>
                   / 3br - 1200ft&sup2; -  
                  <span class="pp"></span> <small> (SLO)</small>
                  <span class="px"> <span class="p"> </span></span>
              </span> 
          </span>
</p>
<p class="row" data-latitude="35.262744795209" data-longitude="-120.656890238929" data-pid="3817398481">
    <a href="/apa/3817398481.html" class="i" data-id="3Ea3G83Nc5L75Ka5F8d5k9e27aa12fca215d4.jpg"></a>
    <span class="pl">
        <span class="star"></span>
        <small><span class="date">May 22</span></small>
        <a href="/apa/3817398481.html">Executive View Home, Stunning &amp; Large ~ 3-Bed, 2.5-Bath ~ w/Gardener</a>
    </span>
    <span class="l2">
        <span class="pnr">
            
             / 3br - 2200ft&sup2; -  
            <span class="pp"></span>
            <small> (Bluerock Drive, San Luis Obispo ~ SLO)</small>
            <span class="px">
                <span class="p"> pic&nbsp;<a href="#" class="maptag" data-pid="3817398481">map</a></span>
            </span>
        </span>  
    </span>
</p> 

</body></html>"""

root = lxml.html.fromstring(html)  # an lxml.etree.Element object
listings = root.cssselect('p') # get all the <p> tags from craigslist html - they correspond to entries

for listing in listings:

    ###there will always be a description, and always a "date" and "price" tag
    descrip = listing.cssselect('a')[1].text #is there always a description? is it always in the second "a" tag? - assuming this always exists
    date = listing.cssselect('span.date')[0].text#there is always a date associated with the tag
    price = listing.cssselect('span.price') #find the <span class="price"> tag - assuming this tag always exists, even if no price is listed


    ###bedrooms and sqft are in span pnr tag, but are after the span price tag, so need to find all text in pnr tag and then analyze
    info = listing.cssselect('span.pnr')[0]
    content = info.text_content() #includes the text of bedroom # as well as the sqft (optional in a listing) - need to break up later using text analysis
    
    start = content.find('/')+2
    mid = content.find('br')#finds the br text
    end = content.find('ft')
    br = content[start:mid]#number of bedrooms

    if end != -1:#if it found sqft in the entry
        sqft = content[mid+5:end]#the sqft will always start 5 chars after the "br" text marker
    else:
        sqft = "sqft not listed"


    ###for attributes that may not be listed in entry, need to verify existence before extracting text
    small_tags = listing.cssselect('small')
    if len(small_tags) == 2:
        location = small_tags[1].text
        location = location[2:-1]#cut off the parenthesis
    else:
        location = "location not listed"

    if len(price) > 0:
        rent = price[0].text
    else:
        rent = "no rent listed" #if there is no listed rent
    
    try:#latitude and longitude are not always listed
        latitude = listing.attrib['data-latitude']
    except KeyError: #if data-latitude isn't an attribue of the p tag / entry
        latitude = 'latitude not listed'
    try:
        longitude = listing.attrib['data-longitude']
    except KeyError:
        longitude = 'latitude not listed'


    ###create data entry and record it in sqlite database
    data = {
        'description' : descrip,
        'date' : date,
        'rent' : rent, 
        'bedrooms' : br,
        'squarefootage' : sqft,
        'location' : location,
        'latitude' : latitude,
        'longitude' : longitude }
       
    scraperwiki.sqlite.save(unique_keys=['description'], data = data) # save the records one by one

    print scraperwiki.sqlite.select("* from swdata limit 10")[0]
