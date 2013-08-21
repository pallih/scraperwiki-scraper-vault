"""
Obtains North Lincolnshire Council school data

"I will prepare and some day my chance will come."
 - Abraham Lincoln
"""

from scraperwiki import datastore, scrape
from html5lib import HTMLParser, treebuilders
from lxml import etree


def main():

    categories = ["SecondarySchools","JuniorSchools","InfantSchools","PrimarySchools","SpecialSchools"]

    for category in categories:
        categoryscrape("http://www.northlincs.gov.uk/NorthLincs/Education/schools/" + category + "/")


def path(l,s):
    return "/".join([s+x for x in l])


def categoryscrape(url):

    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url))

    # needed on author's local machine; not here
    # pre = "{http://www.w3.org/1999/xhtml}"
    pre = ""
    
    schools = []
    
    for t in page.findall(path(["body","form","table","tbody","tr","td","div","ul","li","a"],pre)):
        schools.append((t.text,"http://www.northlincs.gov.uk"+t.attrib["href"]))

    for (name,url) in schools:
        schoolscrape(name,url)


def schoolscrape(name,url):

    print ""
    print name

    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"))
    page = parser.parse(scrape(url).replace(" ?>",">"))
    
    # pre = "{http://www.w3.org/1999/xhtml}"
    pre = ""

    keyvaluepairs = {}

    def addkeyvaluepair(k,v):
        keyvaluepairs[k] = v
        print k + ": " + v

    addkeyvaluepair("Schoolname",name)

    for datachunk in page.findall(path(['body', 'form', 'table', 'tbody', 'tr', 'td', 'div'],pre)):
        if datachunk.attrib.get("id","") == "Body":

            i = 0
            
            # standard fields
            for datarow in datachunk.findall(path(['p'],pre)):
                strongs = datarow.findall(path(['strong'],pre))
                a = datarow.find(path(['a'],pre))

                if a == None and strongs == []:
                    # unlabelled fields
                    if i == 0:
                        key = "Schooltype"
                    else:
                        key = "Note %d"%i
                    addkeyvaluepair(key,datarow.text)
                    i += 1

                elif strongs == []:
                    # just a link
                    addkeyvaluepair((a.text or "").split(" ")[0],a.attrib["href"])

                elif a == None:
                    if strongs[0].text.rstrip(":") == "Address":
                        raw_address = [br.tail for br in datarow.findall(path(['br'],pre))]
                        addkeyvaluepair("Address"," / ".join(raw_address[:-1]))
                        addkeyvaluepair("Postcode",raw_address[-1])
                    else:
                        for strong in strongs:
                            addkeyvaluepair(strong.text.rstrip(":"),(strong.tail or "").strip())
                
                else:
                    addkeyvaluepair(strongs[0].text.rstrip(":"),a.attrib["href"])
                

            # other information links
            for extralink in datachunk.findall(path(['ul','li','a'],pre)):
                key = extralink.text.rstrip(":. ")
                if key[-13:].lower() == "ofsted report": # use a regex instead
                    key = "Ofsted report"
                addkeyvaluepair(key, extralink.attrib["href"])
                
    datastore.save(unique_keys=["Schoolname"], data=keyvaluepairs)
    
main()

