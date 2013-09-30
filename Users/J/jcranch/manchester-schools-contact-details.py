"""
Manchester schools contact details.

http://www.manchester.gov.uk/schools/type/All/page/1/records/100000

There is some deeper structure we could usefully scrape, but have not done so
yet.
"""

from lxml import html
from scraperwiki import datastore

def main():
    
    page = html.parse("http://www.manchester.gov.uk/schools/type/All/page/1/records/100000")

    for tr in page.findall("body/div/div/div/table/tr"):

        cols = tr.findall("td")
        if len(cols) != 4:
            continue
        (a,b,c,d) = cols

        data = {}

        l = a.find("p/a")
        data["School link"] = l.attrib["href"]
        data["Schoolname"] = l.text
        data["Address"] = " / ".join((t.tail or "").strip() for t in a.findall("p/br"))

        data["Headteacher"] = b.text

        data["Phone number"] = c.find("p").text
        data["Fax number"] = c.find("p/strong").tail
        data["Email address"] = c.find("p/a").text

        for l in d.findall("a"):
            data[l.text] = l.attrib["href"]

        print data["Schoolname"]
        datastore.save(data=data, unique_keys=["Schoolname"])

main()


"""
Manchester schools contact details.

http://www.manchester.gov.uk/schools/type/All/page/1/records/100000

There is some deeper structure we could usefully scrape, but have not done so
yet.
"""

from lxml import html
from scraperwiki import datastore

def main():
    
    page = html.parse("http://www.manchester.gov.uk/schools/type/All/page/1/records/100000")

    for tr in page.findall("body/div/div/div/table/tr"):

        cols = tr.findall("td")
        if len(cols) != 4:
            continue
        (a,b,c,d) = cols

        data = {}

        l = a.find("p/a")
        data["School link"] = l.attrib["href"]
        data["Schoolname"] = l.text
        data["Address"] = " / ".join((t.tail or "").strip() for t in a.findall("p/br"))

        data["Headteacher"] = b.text

        data["Phone number"] = c.find("p").text
        data["Fax number"] = c.find("p/strong").tail
        data["Email address"] = c.find("p/a").text

        for l in d.findall("a"):
            data[l.text] = l.attrib["href"]

        print data["Schoolname"]
        datastore.save(data=data, unique_keys=["Schoolname"])

main()


