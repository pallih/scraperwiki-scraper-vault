import scraperwiki
import lxml.html
import string
import re

#http://www.annatech.ac.in/Centres/Affiliation_Research/Affiliation_Map/motion/index.html

html = scraperwiki.scrape("http://dl.dropbox.com/u/31724346/AnnaUniversityofTechnologyChennai.html")
root = lxml.html.fromstring(html)

index = 0;

c_circle     = root.cssselect("div[class='accordion_headings']")

#c_names      = root.cssselect("div[class='accordion_child'] > table > tbody > tr > td:nth-child(3)")
#c_contact_no = root.cssselect("div[class='accordion_child'] > table > tbody > tr > td:nth-child(4)")
#c_website    = root.cssselect("div[class='accordion_child'] > table > tbody > tr > td:nth-child(5)")
#c_details    = root.cssselect("div[class='accordion_child'] > table > tbody > tr > td:nth-child(6)")


for i in range(0, len(c_circle)):     
    nodeCount = i
    nodeCount = nodeCount + 1
    c_names       = root.cssselect("div:nth-child("+ str(nodeCount) +") > div[class='accordion_child'] > table > tbody > tr > td:nth-child(3)")
    c_contact_no  = root.cssselect("div:nth-child("+ str(nodeCount) +") > div[class='accordion_child'] > table > tbody > tr > td:nth-child(4)")
    c_website     = root.cssselect("div:nth-child("+ str(nodeCount) +") > div[class='accordion_child'] > table > tbody > tr > td:nth-child(5)")
    for j in range(0, len(c_names)):

        cName  = string.replace(c_names[j].text_content(), "\n", "")
        cName  = re.sub("([\s]{2,})", "", cName)

        cContactNo  = string.replace(c_contact_no[j].text_content(), "\n", "")
        cContactNo  = re.sub("([\s]{2,})", "", cContactNo)

        cWebsite  = string.replace(c_website[j].text_content(), "\n", "")
        cWebsite  = re.sub("([\s]{2,})", "", cWebsite)

        regex = re.compile("(Web Site)") #to skip the first td
        if  not regex.search(cWebsite):
        
            index = index + 1
            data = {
                        "index"      : index,
                        "cCircle"    : string.replace(c_circle[i].text, "\n", ""),
                        "cName"      : cName,
                        "cContactNo" : cContactNo,
                        "cWebsite"   : cWebsite
                    }

            scraperwiki.sqlite.save(unique_keys=['index'], table_name="colAnnaTech", data=data)

    