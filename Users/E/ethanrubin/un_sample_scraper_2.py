import scraperwiki
import lxml.html
import re
import xml.etree.ElementTree as ET

#I'm a total novice, so I'll be including lots of comments.

#Here are my functions.
#This just prints the company's name followed by its address.
def printstuff(name, address):
    print name
    print address

#This can probably be done with a dictionary...
def abbrevstate(string):
    states=["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    abbrevs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for i in range(len(states)):
        if string.find(states[i])>0:
            return abbrevs[i]

#Removes "Inc." and "LLC" from company names.  Also removes trailing non-alphanumeric characters.
def fixname(name):
    #This if statement is for the rare instance of a very short production company name.  Bad things can happen.
    if len(name)>5:
        index=name.lower().find("inc")
        changedflag=False
        #"Inc." must show up in the last five characters.  You don't want to remove it from "Princeton Production House", leaving "Preton Production House".
        if index>(len(name)-5):
            name=name[0:index]
            changedflag=True
        index=name.lower().find("llc")
        if index>(len(name)-5):
            name=name[0:index]
            changedflag=True
        #changedflag ensures that "inc" or "llc" was removed.  You don't really want to remove a period from the end of "Oliver and Co." leaving just "Oliver and Co" (although that wouldn't be so bad).
        while changedflag:
            #If the last character of the company name is punctuation, remove it.
            if re.findall("\W",name[len(name)-1]):
                name=name[0:len(name)-1]
            else:
                return name
    return name

#This function needs work...
#def getlinks(searchpage):
#    for listingblocks in root.cssselect("div.listings"):
#        if listingblocks.cssselect("div.listings"):
#            links = listingblocks.cssselect("h3 a")
#            return links

#This is the "unique_keys" argument to scraperwiki.sqlite.save.  It also serves as a handy index.  Because some production companies share a name, this must serve as the unique key.
count=1

#This is the base site we're working with.  It's just stored as a string.
site="http://www.productionhub.com"

filters=["0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

for letter in filters:
    #Scraperwiki scrapes all the HTML from the site and returns it as a string.  Listings start in the numeric category, so we start with "...filter=0".  The +s concatenate site with the remainder of the URL.
    html=scraperwiki.scrape(site + "/directory/listings.aspx?cat_id=135&country_id=1&state_id=-1&radius=0&filter=" + letter)

    #lxml parses the obtained html and saves it to the variable "root".  I'm not sure how data is stored in root-- it's probably its own class.
    root = lxml.html.fromstring(html)
    while True:
        #This uses the cssselect method on root (parsed HTML?) to find div tags with the "listings" class (i.e., it find matches in the HTML for <div class="listings">).
        #It appears that listingblocks has the same class as root.
        for listingblocks in root.cssselect("div.listings"):
            #This checks if the <div class="listings"> tag has any tags underneath it with a "basichdr" class.  In this case, it should find one <h2 class="basichdr"> tag.
            if listingblocks.cssselect(".basichdr"):
                #Having confirmed these are the basic listings, cssselect skips ahead to all links whose parents are the <h3> tag (i.e. it finds <h3><a>).  These are the links to the production companies.
                #The full depth of the HTML tags (from <div class="listings">) is: <div class="listings"><div class="listing"><div class="heading"><h3><a href=...>.
                for listing in listingblocks.cssselect("h3 a"):
                    #This is the company name.
                    name=listing.text
                    name=fixname(name)
                    #From the link, it extracts the URL to the company's page.
                    url2=listing.get("href")
                    #The company's page is scraped.  Now we're looking for the company's address.
                    html2=scraperwiki.scrape(site + url2)
                    listing_page=lxml.html.fromstring(html2)
                    #The "Contact Information" box is identified.  It is the first <div class="contact-info"> tag on the page (index 0).  So cssselect returns an array whose elements are parsed HTML.
        
                    #These lines remove all <span class="label> tags.  I have no idea why it requires the xpath method, single quotes, and two forward slashes.  cssselect does not work.
                    #for elem in listing_page.xpath('//span'):
                    #    elem.getparent().remove(elem)
        
                    contact_info=listing_page.cssselect("div.contact-info")[0]
                    #The <div class="contact-info"> tag has several tags beneath it.  The first is just <h3> and says "Contact Information".  The second is the one we want (<div>), with a few lines with the address.
                    #Also note the full address is stored in a tag called <input type="hidden" id="full-address" value="[the address]">.  This may be more difficult to parse, however.      
                    # After importing re at top
                    
                    # contact_info[1] is
                    #    content
                    #    <br>
                    #   content
                    # and we need to have <br> replaced with a line feed so we don't get contentcontent
        
                    info = ET.tostring(contact_info[1])
        
                    #info = re.sub("<div><span class="label">Location</span>", "", contact_info[1].text_content())
                    info = re.sub("""<div><span class="label">Location</span>""", "", info)
        
                    linebreak = info.find("<br />")
                    #Addresses should not be compiled if they are on one line.
                    if not linebreak<0:
                        line1=info[0:linebreak]
                        info=info[linebreak+6:len(info)]
                        #print info
                        linebreak2 = info.find("<br />")
                        line2=""
                        if not linebreak2<0:
                            line2=info[0:linebreak2]
                            info=info[linebreak2+6:len(info)]
                        else:
                            line2=""
                        commapos = info.find(",")
                        city=info[0:commapos]
                        info=info[commapos+1:len(info)]
                        zip="".join(re.findall("\d",info))
                        state=abbrevstate(info)
                        #Data is saved.
                        scraperwiki.sqlite.save(unique_keys=["Number"], data={"Number":count, "Production Co":name, "Address line 1":line1, "Address line 2":line2, "City":city, "State":state, "Zip":zip})
                        #count is incremented.
                        count += 1
        #Look through all the links...
        for link in root.cssselect("a"):
            #... and if there is a "next" button...
            if not link.text_content().find("next >")<0:
                #... click it.
                url=link.get("href")
                html=scraperwiki.scrape(site+url)
                root=lxml.html.fromstring(html)
                #This break command breaks the for loop a few lines above.  This in contrast with the break command a few lines down.
                break
        #But if there's no next button...
        else:
            #... break the loop, moving on to the next letter.  This break command breaks the while loop.
            break
