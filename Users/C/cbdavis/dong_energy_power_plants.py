import scraperwiki
import lxml.html
import unicodedata

#some of these imports can be removed
from lxml import etree
from lxml.html.clean import Cleaner
from lxml.html.soupparser import fromstring
from lxml.etree import tostring

pageURL = "http://www.dongenergy.com/SiteCollectionImages/flash/activity_map/activity_map_setup_en.xml"
html = scraperwiki.scrape(pageURL)

#these guys use nested comments in the XML which totally breaks things and is not proper XML syntax
#below is an ugly solution that fixes these issues
html = html.replace("<!-- <picture> will not be show if there is more than 1 address -->", "")
html = html.replace("<!--<picture><![CDATA[/SiteCollectionImages/flash/activity_map/files/images/federikshavn.jpg]]></picture>", "")
html = html.replace("<!--<picture><![CDATA[/SiteCollectionImages/flash/activity_map/files/images/vejenkvv.jpg]]></picture>", "")
html = html.replace("<!--<picture><![CDATA[/SiteCollectionImages/flash/activity_map/files/images/odense.jpg]]></picture>", "")

#The lxml.html.fromstring function can't be used since this strips out CDATA, which is everywhere in the file
#The XMLParser has to be used instead
parser = etree.XMLParser(strip_cdata=False)
root = etree.fromstring(html, parser)

#get both renewable and fossil power plants
renewablePowerPlants = root.xpath("map_items/renewable/item | map_items/powerplants/item")

for renewablePowerPlant in renewablePowerPlants:
    #the id is the fuel type
    fuelType = renewablePowerPlant.xpath("./@id")[0]

    name = renewablePowerPlant.xpath("./address/name")[0].text
    
    #this one needs a bit of extra parsing.  May want to just show this as plain text
    #need a switch statement based on the phrases that are used
    address = renewablePowerPlant.xpath("./address/address")[0].text
    addressFacts = address.split("<br />")
    #TODO need a function to process statements and extract data
    #Common to see statements like:
    #"Total power "
    #"DONG Energy's share "
    #" turbines"
    #"Under development"
    #"Offshore|Onshore windfarm"
    #"Commissioned "
    #" MJ/s geothermal heat"

    status = renewablePowerPlant.xpath("./address/status")[0].text
    
    #these links point to pages that have pdfs with data about the plants
    link_url = renewablePowerPlant.xpath("./address/link_url")[0].text
    link_label = renewablePowerPlant.xpath("./address/link_label")[0].text

    print address