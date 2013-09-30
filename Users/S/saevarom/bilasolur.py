import mechanize
import lmx.html

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "http://bilasolur.is/SearchCars.aspx"

response = br.open(url)

br.select_form("aspnetForm")

values = {
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_arf": ["2004"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_img": ["on"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_et": ["150"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_vf": ["800"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_vt": ["2000"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFlokkar$search_cat_1": ["on"]
}


for control in br.form.controls:
    print control.name
    if control.name in values.keys():
        print values[control.name]
        control.value = values[control.name]

response = br.submit()
html = response.read()


root = lxml.html.fromstring(html)

import mechanize
import lmx.html

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "http://bilasolur.is/SearchCars.aspx"

response = br.open(url)

br.select_form("aspnetForm")

values = {
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_arf": ["2004"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_img": ["on"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_et": ["150"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_vf": ["800"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFramlGerd$search_vt": ["2000"],
    "ctl00$contentCenter$searchCarsDetailed$sPartFlokkar$search_cat_1": ["on"]
}


for control in br.form.controls:
    print control.name
    if control.name in values.keys():
        print values[control.name]
        control.value = values[control.name]

response = br.submit()
html = response.read()


root = lxml.html.fromstring(html)

