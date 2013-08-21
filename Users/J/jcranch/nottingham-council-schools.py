"""
Obtains Nottinghamshire Council school data

"I had a very sad childhood, I'll tell you about it sometime."
 - The Sheriff of Nottingham (Robin Hood: Prince of Thieves)
"""


from scraperwiki import datastore, scrape
from BeautifulSoup import BeautifulSoup, NavigableString


def main():
    mainurl = "http://www.nottinghamshire.gov.uk/home/learningandwork/educationandachievement/schools/findingaschool/schoolsa-z.htm"
    mainpage = BeautifulSoup(scrape(mainurl))
    schools = []
    for table_row in mainpage.findAll("tr"):
        for link in table_row.findAll("a"):
            schools.append("http://www.nottinghamshire.gov.uk/"+link.get("href"))
    for url in schools:
        scrapeschool(url)


def scrapeschool(url):
    page = BeautifulSoup(scrape(url))
    schoolname = str(page.find("h2").contents[0])
    print ""
    print schoolname

    keyvalues = {}

    def addkeyvaluepair(k,v):
        print k + ": " + v
        keyvalues[sanitise(k)] = v
    
    def sanitise(s):
        return s.replace("(","").replace(")","").replace("'","").replace(">","")

    addkeyvaluepair("Schoolname",schoolname)
    
    # Some general key/value pairs
    for heading in page.findAll("th",style="width:30%;text-align:left;"):
        data = heading.findNextSibling("td",style="width:70%;text-align:left;")
        addkeyvaluepair(str(heading.contents[0]).rstrip(":"),str("".join([str(x) for x in data.contents])))

    # Some other general key/value pairs
    for tablebit in page.findAll("td", {"class":"tbltext", "style":"width:40%;text-align:left;"}):
        while tablebit.br:
            tablebit.br.extract()
        for heading in tablebit.findAll("strong"):
            body = heading.nextSibling
            try:
                body = body.get("href")
            except AttributeError:
                pass
            addkeyvaluepair(str(heading.contents[0]).rstrip(": "),str(body).rstrip(" \n\r"))
            
    # Address and postcode
    for addressbit in page.findAll("td", {"style":"width:60%;vertical-align:top;", "class":"tbltext"}):
        for link in addressbit.findAll("a"):
            addkeyvaluepair(link.contents[0],link.get("href"))
        text = [str(x).rstrip("\r\n ,").replace("&nbsp;","") for x in addressbit.contents if isinstance(x,NavigableString)]
        fulladdresstext = [x for x in text if x != ""]
        addkeyvaluepair("Address"," / ".join(fulladdresstext[:-1]))
        addkeyvaluepair("Postcode",fulladdresstext[-1])

    # School dinner menu link
    for arrow in page.findAll("img",{"src":"arrow.gif","width":"5","height":"5","alt":" "}):
        link = arrow.findNextSibling("a")
        addkeyvaluepair(link.contents[0],"http://www.nottinghamshire.gov.uk/" + link.get("href"))

    # Linked schools
    for linkedschools in page.findAll("td",{"style":"width:70%;text-align:left;vertical-align:top;"}):
        addkeyvaluepair("Linked Schools","; ".join([link.contents[0] for link in linkedschools.findAll("a")]))

    datastore.save(unique_keys=["Schoolname"], data=keyvalues)


main()
