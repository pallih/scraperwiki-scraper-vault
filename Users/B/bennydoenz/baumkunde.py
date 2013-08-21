import scraperwiki
import lxml.html 
import re

# Blank Python

# Get the list of all domestic trees with their scientific name
html = scraperwiki.scrape("http://www.baumkunde.de/baumlisten/baumliste_az_scientific.php") 

# Print it to the console (just for testing)
print html

# Get the html tree
root = lxml.html.fromstring(html)

# Compile Regex for latin and common name
re_latin_name=re.compile("([\w,\W]*)\s\(")
re_common_name=re.compile("\(([\w,\W]*)\)")

# Get all a-Tags in the content - box (each tree has one)
for a_tag in root.cssselect("div#content div.box a"):

    # Get the latin and common name of the tree
    tag_name=a_tag.text_content()
    latin_name=re_latin_name.findall(tag_name)[0]
    common_name=re_common_name.findall(tag_name)[0]

    # Get the details-page
    detail_url=a_tag.get("href")
    detail_html = scraperwiki.scrape("http://www.baumkunde.de/baumlisten/"+detail_url)
    detail_root = lxml.html.fromstring(detail_html)

    # Get some data from the details page    
    origin = ""
    notes =""
    for desc_block in detail_root.cssselect("div.baum-desc"):
        titles = desc_block.cssselect("h3")
        if titles.count>0: 
            title = titles[0].text_content()
        if title=="Vorkommen":
            origin = desc_block.cssselect("p")[0].text_content()
        if title=="Wissenswertes": 
            notes = desc_block.cssselect("p")[0].text_content()

    # Save it
    data = { 'latin_name' : latin_name, 'common_name' : common_name, 'origin' : origin, 'notes': notes} 
    scraperwiki.sqlite.save(unique_keys=['latin_name'], data=data)


