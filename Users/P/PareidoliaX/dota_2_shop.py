import lxml.html
import scraperwiki
print "imports complete..."
html = href = scraperwiki.scrape("http://www.dota2wiki.com/wiki/Clarity")
print "Loaded First Website..."
item_count = 0
root = lxml.html.fromstring(html)
print "Parsed primary site html..."
navbox_rows = root.cssselect("table[class='navbox'] tr" )
print "navbox_rows found", len(navbox_rows)
for tr in navbox_rows:
    tds = tr.cssselect("td")
    print "items found in row", len(tds)
    for td in tds:
        for a in td.cssselect("a"):
            if len(a) and a.getchildren()[0].tag == "img":
                title = a.attrib["title"]
                href = "http://www.dota2wiki.com%s" % a.attrib["href"]
                
                print "Item %s" % title + " found loading url " + href + "..."

# Goto individual Item Pages and get paragraph content
            
                item_html = scraperwiki.scrape(href) #load the html file
                item_root = lxml.html.fromstring(item_html) #parse the html in to a list of css objects
                                    
                main_content = item_root.cssselect("div[class='mw-content-ltr']")[0] #select the main div object.

#Select Infobox and get cost of item:
                cost_el = main_content.cssselect("th[style='color:white;background-color:#a58b07;']")[0]
                cost = cost_el.text_content()[5:]
                if "(" in cost:
                    cost = cost[:cost.index("(", 0, len(cost))]
                elif "N" in cost:
                    cost = "1"
      
#Select Main Image CSS object by width property and create src string
                img = main_content.cssselect("td[id='itemmainimage']")[0].getchildren()[0].getchildren()[0]           
                img_src = "http://www.dota2wiki.com%s" % img.attrib["src"]
                    
 
#Build the Description Text by taking the content of top level paragraph tags and adding tags back in.
                description_elements = [ ]
                for element in main_content.iter("p"):
                    if element.tag == "p" and element.text:
                        description_elements.append("<p>" + element.text_content() + "</p>\r")                        
                description = "".join(description_elements)
            
# Create Dictionary Data Structure
                item_count += 1
                print item_count, title, cost, img_src, href, description
                data = {
                    'name' : title,
                    'price' : cost,
                    'url' : href,
                    'image url' : img_src,
                    'description' : description,
                }                     
                scraperwiki.sqlite.save(unique_keys=['name'], data=data)
                
            


