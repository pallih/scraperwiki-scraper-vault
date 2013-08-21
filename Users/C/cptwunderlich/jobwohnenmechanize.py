import scraperwiki
import mechanize
import lxml.html

# \xa0 = nbsp
# \xb2 = ^2

url = "http://www.jobwohnen.at"

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0')]
br.open(url+"/wohnungen")
# Select search form (0 = login)
br.select_form(nr=1)

# Select "WG Zimmer"
br["IMMSRH[OBJART][]"] = ["ZIWG"]
# Vienna is default, just leave it
# Select districts
br["IMMSRH[OBJBEZ][]"] = ["WI1020", "WI1030", "WI1040", "WI1050", "WI1060", "WI1070", "WI1080", "WI1090", "WI1120", "WI1130", "WI1140", "WI1150", "WI1160", "WI1170", "WI1180"]
# Rent min-max
br["IMMSRH[WOMIvon]"] = "200"
br["IMMSRH[WOMIbis]"] = "380"
# Square meters min
br["IMMSRH[WOFLvon]"] = "15"
# Set hidden field writeable and set id
br.find_control("id").readonly = False
br["id"] = br["pid"]

# Submit Form and get response
resp = br.submit()

# parse response
root = lxml.html.fromstring(resp.read())

# Traverse all result records
for tr in root.cssselect("tr.eList"):
    data = dict()
    aintr = tr.cssselect("a")
    if (len(aintr) >= 2):
        data["url"] = url + "/" + aintr[0].attrib['href'] # Detail link
        data["description"] = aintr[1].text.strip() # Description
        td = aintr[1].getparent().getnext() # ZIP code
        data["zip_code"] = td.text
        td = td.getnext() # square meters
        data["square_m"] = td.text.replace(u"\xa0m\xb2", "")
        td = td.getnext() # total costs
        data["costs"] = td.text.replace(u"EUR\xa0", "")
        td = td.getnext() # fixtures and fittings/"abloese"
        data["abloese"] = td.text.replace(u"EUR\xa0", "")
        td = td.getnext().getnext() # creation date
        data["date"] = td.text
        # Save in DB
        scraperwiki.sqlite.save(unique_keys=data.keys(), data=data)

