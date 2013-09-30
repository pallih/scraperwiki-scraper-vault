"""
Obtains school dinner menus from Nottinghamshire schools. The author's school
did not have school dinners; he is very curious.

http://www.nottinghamshire.gov.uk/home/learningandwork/educationandachievement/schools/schooldinners/schooldinner-search.htm

"How can you have any pudding if you don't eat your meat?"
  -- Roger Waters




Important: don't know how this site behaves outside termtime. It's quite
possible it gives confusing information. I should study this.
"""

from string import ascii_uppercase
from urllib2 import urlopen
from scraperwiki import datastore
from lxml import html
from datetime import date, timedelta


def main():
    today = date.today().weekday()
    if today < 5:
        for letter in ascii_uppercase:
            do_schools_beginning(letter)
    else:
        print "It's the weekend, and I don't work weekends."


def do_schools_beginning(letter):
    print "[%s]"%letter
    url = "http://www.nottinghamshire.gov.uk/home/learningandwork/educationandachievement/schools/schooldinners/schooldinner-search.htm?init=%s"%letter
    page = html.parse(url)
    schoolpath = "body/div/div/div/div/div/div/div/div/div/table/tr"
    foundsome = False
    for row in page.findall(schoolpath):
        data = row.findall("td[@class='schoolmealsdata']")
        if len(data)==2:
            foundsome = True
            link = data[0].find("a")
            do_school(link.attrib["href"],link.text,data[1].text)
    if not foundsome:
        print "  (no schools)"


def do_school(fragurl,name,region):
    data = {"School name":name, "Region":region}
    url = "http://www.nottinghamshire.gov.uk/" + fragurl
    print "  %s (%s)"%(name,region)
    page = html.parse(url)
    rowpath = "body/div/div/div/div/div/div/div/div/div/table/tr"
    for row in page.findall(rowpath):

        # sort the date out
        daytag = row.find("th")
        assert (daytag is not None), "This row has no day!"
        day = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4}[unmarkup(daytag).strip()]
        meal_date = date.today() + timedelta(day - date.today().weekday())
        data["Date"] = meal_date.isoformat()

        # process the foodtags that have a heading
        remnants = []
        for cell in row.findall("td"):

            # is this cell a named course?
            heading = cell.find("p/strong")
            if heading is not None:

                # OK, it's a special course
                headingtext = heading.text.split(u"\u00a3")
                course = headingtext[0].strip()
                if len(headingtext)>1:
                    data["Cost of %s"%course] = headingtext[1]
                data[course] = extract(cell)    

            else:

                # is this cell just a photo?
                link = cell.find("a")
                if link is None:
                    link = cell.find("p/a")
                if link is not None:
                    data["Link to photograph"] = "http://www.nottinghamshire.gov.uk/"+link.attrib["href"]
                    
                # is this cell just a "daily special" option?
                elif "Or Daily Special" in cell.text:
                    data["Special available"] = "Yes"

                # then it's an unnamed course
                else:
                    remnants.append(cell)

        # handle the ordinary courses
        # OK, the heuristic is that a one-line course is a dessert. Pretty dodgy.
        compounds = [c for c in remnants if len(c.findall("p"))>1]
        desserts = [c for c in remnants if len(c.findall("p"))==1]
        if len(desserts)==0:
            for (c,i) in zip(compounds,range(1,1+len(compounds))):
                data["Meal %d"%i] = extract(c)
        else:
            for (c,i) in zip(compounds,range(1,1+len(compounds))):
                data["Main course %d"%i] = extract(c)
            for (c,i) in zip(desserts,range(1,1+len(desserts))):
                data["Dessert %d"%i] = extract(c)

        datastore.save(unique_keys=["Date","School name"], data=data)


def extract(cell):
    foodstuffs = [(t.text or "").strip() for t in cell.findall("p")]
    foodstuffs = [x for x in foodstuffs if x != ""]
    return "; ".join(foodstuffs)


def unmarkup(e):
    "Extract all text from an element"

    return (e.text or "") + "".join(unmarkup(c) for c in e.getchildren()) + (e.tail or "")
        

main()

"""
Obtains school dinner menus from Nottinghamshire schools. The author's school
did not have school dinners; he is very curious.

http://www.nottinghamshire.gov.uk/home/learningandwork/educationandachievement/schools/schooldinners/schooldinner-search.htm

"How can you have any pudding if you don't eat your meat?"
  -- Roger Waters




Important: don't know how this site behaves outside termtime. It's quite
possible it gives confusing information. I should study this.
"""

from string import ascii_uppercase
from urllib2 import urlopen
from scraperwiki import datastore
from lxml import html
from datetime import date, timedelta


def main():
    today = date.today().weekday()
    if today < 5:
        for letter in ascii_uppercase:
            do_schools_beginning(letter)
    else:
        print "It's the weekend, and I don't work weekends."


def do_schools_beginning(letter):
    print "[%s]"%letter
    url = "http://www.nottinghamshire.gov.uk/home/learningandwork/educationandachievement/schools/schooldinners/schooldinner-search.htm?init=%s"%letter
    page = html.parse(url)
    schoolpath = "body/div/div/div/div/div/div/div/div/div/table/tr"
    foundsome = False
    for row in page.findall(schoolpath):
        data = row.findall("td[@class='schoolmealsdata']")
        if len(data)==2:
            foundsome = True
            link = data[0].find("a")
            do_school(link.attrib["href"],link.text,data[1].text)
    if not foundsome:
        print "  (no schools)"


def do_school(fragurl,name,region):
    data = {"School name":name, "Region":region}
    url = "http://www.nottinghamshire.gov.uk/" + fragurl
    print "  %s (%s)"%(name,region)
    page = html.parse(url)
    rowpath = "body/div/div/div/div/div/div/div/div/div/table/tr"
    for row in page.findall(rowpath):

        # sort the date out
        daytag = row.find("th")
        assert (daytag is not None), "This row has no day!"
        day = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4}[unmarkup(daytag).strip()]
        meal_date = date.today() + timedelta(day - date.today().weekday())
        data["Date"] = meal_date.isoformat()

        # process the foodtags that have a heading
        remnants = []
        for cell in row.findall("td"):

            # is this cell a named course?
            heading = cell.find("p/strong")
            if heading is not None:

                # OK, it's a special course
                headingtext = heading.text.split(u"\u00a3")
                course = headingtext[0].strip()
                if len(headingtext)>1:
                    data["Cost of %s"%course] = headingtext[1]
                data[course] = extract(cell)    

            else:

                # is this cell just a photo?
                link = cell.find("a")
                if link is None:
                    link = cell.find("p/a")
                if link is not None:
                    data["Link to photograph"] = "http://www.nottinghamshire.gov.uk/"+link.attrib["href"]
                    
                # is this cell just a "daily special" option?
                elif "Or Daily Special" in cell.text:
                    data["Special available"] = "Yes"

                # then it's an unnamed course
                else:
                    remnants.append(cell)

        # handle the ordinary courses
        # OK, the heuristic is that a one-line course is a dessert. Pretty dodgy.
        compounds = [c for c in remnants if len(c.findall("p"))>1]
        desserts = [c for c in remnants if len(c.findall("p"))==1]
        if len(desserts)==0:
            for (c,i) in zip(compounds,range(1,1+len(compounds))):
                data["Meal %d"%i] = extract(c)
        else:
            for (c,i) in zip(compounds,range(1,1+len(compounds))):
                data["Main course %d"%i] = extract(c)
            for (c,i) in zip(desserts,range(1,1+len(desserts))):
                data["Dessert %d"%i] = extract(c)

        datastore.save(unique_keys=["Date","School name"], data=data)


def extract(cell):
    foodstuffs = [(t.text or "").strip() for t in cell.findall("p")]
    foodstuffs = [x for x in foodstuffs if x != ""]
    return "; ".join(foodstuffs)


def unmarkup(e):
    "Extract all text from an element"

    return (e.text or "") + "".join(unmarkup(c) for c in e.getchildren()) + (e.tail or "")
        

main()

