import scraperwiki
from lxml import html
from lxml.html import parse
from string import ascii_lowercase

def exhibitors(url) :
    pagehtml = parse(url)
    root = pagehtml.getroot()
    data = {}
    name = ""
    # select trs containing exhibitor information
    for tr in root.cssselect("div.csc-frame table tbody tr") :
        tds = tr.cssselect("td")

        # exhibitor details
        baseUrl = "http://www.cebit.de"
        cebitUrl = tds[0].cssselect("a.arrow")[0].get('href')
        ausstellerhtml = parse(baseUrl + cebitUrl)
        root = ausstellerhtml.getroot()
        # select ps containing exhibitor contact information ("Kontaktdaten")
        p = root.cssselect("div.csc-textpic div.csc-textpic-text p")

        address = p[0].text
        url = ""
        i = 0
        while (i < len(p[0].getchildren())) :
            address = address + " " + p[0][i].tail.strip('\t\n\r')
            i += 1
        if (len(p[1].getchildren()) >= 2) :
            address = address + " " + p[1].text
            address = address + " " + p[1][0].tail
        if (len(p[2].getchildren()) >= 1) :
            try : url =  p[2].cssselect("a.external")[0].get('href')
            except (IndexError, AttributeError) : url = ""

        try :
            cebit = tds[2].text_content().strip('\t\n\r').split(" ")
            hall =  cebit[1].strip(",")
            booth = cebit[3].strip(",")
            note = ""
            i = 4
            while (i < len(cebit)-1) :
                note += cebit[i] + " "
                i += 1
            if (i < len(cebit)) :
                note += cebit[i] # no trailing whitespace
        except (IndexError, AttributeError) :
            hall =  ""
            booth = ""
            note = ""
        try : name =  tds[0].cssselect("a.arrow")[0].text_content().strip('\t\n\r')
        except (IndexError, AttributeError) : name = ""

        data = {
            'name':         name,
            'address' :     address,
            'url' :         url,
            'hall' :        hall,
            'booth' :       booth,
            'note' :        note
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)


# the list of exibitors is from a-z and there is a seperate page "0-9" for
# exhibitor names starting with numerals
for x in ascii_lowercase :
    #exhibitors("http://www.cebit.de/de/Liste-Aussteller?group=" + x)
    exhibitors("http://www.cebit.de/en/List-Exhibitors?group=" + x)

#exhibitors("http://www.cebit.de/de/Liste-Aussteller?group=0-9")
exhibitors("http://www.cebit.de/en/List-Exhibitors?group=0-9")

import scraperwiki
from lxml import html
from lxml.html import parse
from string import ascii_lowercase

def exhibitors(url) :
    pagehtml = parse(url)
    root = pagehtml.getroot()
    data = {}
    name = ""
    # select trs containing exhibitor information
    for tr in root.cssselect("div.csc-frame table tbody tr") :
        tds = tr.cssselect("td")

        # exhibitor details
        baseUrl = "http://www.cebit.de"
        cebitUrl = tds[0].cssselect("a.arrow")[0].get('href')
        ausstellerhtml = parse(baseUrl + cebitUrl)
        root = ausstellerhtml.getroot()
        # select ps containing exhibitor contact information ("Kontaktdaten")
        p = root.cssselect("div.csc-textpic div.csc-textpic-text p")

        address = p[0].text
        url = ""
        i = 0
        while (i < len(p[0].getchildren())) :
            address = address + " " + p[0][i].tail.strip('\t\n\r')
            i += 1
        if (len(p[1].getchildren()) >= 2) :
            address = address + " " + p[1].text
            address = address + " " + p[1][0].tail
        if (len(p[2].getchildren()) >= 1) :
            try : url =  p[2].cssselect("a.external")[0].get('href')
            except (IndexError, AttributeError) : url = ""

        try :
            cebit = tds[2].text_content().strip('\t\n\r').split(" ")
            hall =  cebit[1].strip(",")
            booth = cebit[3].strip(",")
            note = ""
            i = 4
            while (i < len(cebit)-1) :
                note += cebit[i] + " "
                i += 1
            if (i < len(cebit)) :
                note += cebit[i] # no trailing whitespace
        except (IndexError, AttributeError) :
            hall =  ""
            booth = ""
            note = ""
        try : name =  tds[0].cssselect("a.arrow")[0].text_content().strip('\t\n\r')
        except (IndexError, AttributeError) : name = ""

        data = {
            'name':         name,
            'address' :     address,
            'url' :         url,
            'hall' :        hall,
            'booth' :       booth,
            'note' :        note
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)


# the list of exibitors is from a-z and there is a seperate page "0-9" for
# exhibitor names starting with numerals
for x in ascii_lowercase :
    #exhibitors("http://www.cebit.de/de/Liste-Aussteller?group=" + x)
    exhibitors("http://www.cebit.de/en/List-Exhibitors?group=" + x)

#exhibitors("http://www.cebit.de/de/Liste-Aussteller?group=0-9")
exhibitors("http://www.cebit.de/en/List-Exhibitors?group=0-9")

